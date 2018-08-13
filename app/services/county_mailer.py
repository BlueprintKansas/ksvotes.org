from flask import current_app
from app.models import Clerk
import os
import hashlib
import base64
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import boto3
import botocore

class CountyMailer():

    def __init__(self, registrant, form_img_type, body):
        self.registrant = registrant
        self.form_imgs = registrant.try_value(form_img_type)
        if isinstance(self.form_imgs, str):
            self.form_imgs = [self.form_imgs]
        self.clerk = Clerk.find_by_county(registrant.county)
        if self.clerk == None:
            raise Exception("No Clerk for County %s" %(registrant.county))
        self.set_subject(form_img_type)
        self.body = body

    def set_subject(self, form_img_type):
        subject = 'No Subject'
        if form_img_type == 'ab_forms':
            subject = "New Advance Ballot application(s) for {}".format(self.registrant.name())
        elif form_img_type == 'vr_form':
            subject = "New Voter Registration for {}".format(self.registrant.name())
        else:
            raise Exception("Unknown form_img_type %s" %(form_img_type))

        self.subject = subject

    def clerk_email(self):
        if self.clerk.county == 'TEST':
            return os.getenv('TEST_CLERK_EMAIL', self.clerk.email)
        elif os.getenv('TEST_CLERK_EMAIL'):
            return os.getenv('TEST_CLERK_EMAIL')
        else:
            return self.clerk.email

    def send(self):
        current_app.logger.info("%s SEND mail to %s" %(self.registrant.session_id, self.clerk_email()))
        to = [self.clerk_email()]
        cc = [self.registrant.try_value('email')]
        msg = self.build_msg(
            attach=self.build_attachments(),
            to=to,
            cc=cc,
            bcc=[current_app.config['EMAIL_BCC']],
            subject=self.subject,
        )
        r = self.send_msg(msg, current_app.config['EMAIL_FROM'])
        current_app.logger.info("%s SENT %s" %(self.registrant.session_id, r))
        return r

    def build_attachments(self):
        attachments = []
        m = hashlib.sha256()
        for img_str in self.form_imgs:
            # we just need a unique string for each name -- this is not a security thing.
            m = hashlib.sha256()
            m.update(img_str.encode('utf-8'))
            shasum = m.hexdigest()
            img_bin = base64.b64decode(img_str.replace('data:image/png;base64,', '').replace('"', '').replace("'", ''))
            att = { 'name': str(self.registrant.session_id)+'-'+shasum+'.png', 'img': img_bin }
            attachments.append(att)
        return attachments

    def to_html(self, txt):
        html = '<html><body><p>' + txt.replace("\n", '</p><p>') + '</p></body></html>'
        return html

    def build_msg(self, **kwargs):
        recip_to = kwargs['to'] if 'to' in kwargs else None
        if not recip_to:
            raise('to required')
        recip_cc = kwargs['cc'] if 'cc' in kwargs else []
        recip_bcc = kwargs['bcc'] if 'bcc' in kwargs else []
        subject = kwargs['subject'] if 'subject' in kwargs else ''
        body = kwargs['body'] if 'body' in kwargs else self.body
        attachments = kwargs['attach'] if 'attach' in kwargs else None
        if not attachments:
            raise('attach required')

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['To'] = ', '.join(recip_to)
        msg['Cc'] = ', '.join(recip_cc)
        msg['Bcc'] = ', '.join(recip_bcc)

        # order of mime parts is important, as last is preferred in client view.
        readable_msg = MIMEMultipart('alternative')
        readable_msg.attach(MIMEText(body, 'plain' , 'utf-8'))
        readable_msg.attach(MIMEText(self.to_html(body), 'html', 'utf-8'))
        msg.attach(readable_msg)

        for attachment in attachments:
            file_name = attachment['name']
            mime_part = MIMEApplication(attachment['img'])
            mime_part.add_header('Content-Disposition', 'attachment', filename=file_name)
            mime_part.add_header('Content-Type', 'image/png; name="{}"'.format(file_name))
            msg.attach(mime_part)

        return msg

    def send_msg(self, msg, sender):
        msg['From'] = sender
        # no email sent unless explicitly configured.
        if not current_app.config['SEND_EMAIL']:
            return {'msg': msg, 'MessageId': 'set SEND_EMAIL env var to enable email'}

        try:

            ses = boto3.client('ses',
                region_name=current_app.config['AWS_DEFAULT_REGION'],
                aws_access_key_id=current_app.config['SES_ACCESS_KEY_ID'],
                aws_secret_access_key=current_app.config['SES_SECRET_ACCESS_KEY']
            )
            resp = ses.send_raw_email(
                RawMessage={'Data': msg.as_string()},
                Source=sender,
            )
            return resp

        except botocore.exceptions.ClientError as err:
            current_app.logger.error(str(err))
            return {'msg': msg, 'MessageId': False, 'error': err}

