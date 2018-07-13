from flask import g, current_app
from app.models import Clerk
import hashlib
import base64
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import boto3

class CountyMailer():

    def __init__(self, registrant, form_imgs):
        self.registrant = registrant
        self.form_imgs = form_imgs
        self.clerk = Clerk.find_by_county(registrant.county)
        if self.clerk == None:
            raise Exception("No Clerk for County %s" %(registrant.county))

    def send(self):
        current_app.logger.info("%s SEND mail to %s" %(self.registrant.session_id, self.clerk.email))
        r = self.send_ses(
            attach=self.build_attachments(),
            to=[self.registrant.try_value('email')],
            cc=['peknet+ksvotes@gmail.com'],
            subject='test ksvotes',
        )
        current_app.logger.info("%s SENT %s" %(self.registrant.session_id, r))
        return True # TODO check r

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

    def send_ses(self, **kwargs):
        recip_to = kwargs['to'] if 'to' in kwargs else None
        if not recip_to:
            raise('to required')
        recip_cc = kwargs['cc'] if 'cc' in kwargs else []
        recip_bcc = kwargs['bcc'] if 'bcc' in kwargs else []
        sender = kwargs['from'] if 'from' in kwargs else current_app.config['SES_EMAIL_FROM']
        subject = kwargs['subject'] if 'subject' in kwargs else ''
        body = kwargs['body'] if 'body' in kwargs else 'EMPTY EMAIL'
        attachments = kwargs['attach'] if 'attach' in kwargs else None
        if not attachments:
            raise('attach required')

        ses = boto3.client('ses',
            region_name=current_app.config['AWS_DEFAULT_REGION'],
            aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY']
        )

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recip_to)
        msg['Cc'] = ', '.join(recip_cc)
        msg['Bcc'] = ', '.join(recip_bcc)
        all_addresses = recip_to
        for addr in recip_cc:
            all_addresses.append(addr)
        for addr in recip_bcc:
            all_addresses.append(addr)

        msg.attach(MIMEText(body, 'text'))
        for attachment in attachments:
            file_name = attachment['name']
            mime_part = MIMEApplication(attachment['img'])
            mime_part.add_header('Content-Disposition', 'attachment', filename=file_name)
            #mime_part.add_header('Content-Type', 'image/png; name="{}"'.format(file_name))
            #mime_part.add_header('Content-Transfer-Encoding', 'base64')
            msg.attach(mime_part)

        resp = ses.send_raw_email(
            RawMessage={'Data': msg.as_string()},
            Source=sender,
            Destinations=all_addresses
        )
        # TODO check resp for success?
        return resp

