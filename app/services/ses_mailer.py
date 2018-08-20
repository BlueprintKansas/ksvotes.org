import boto3
import botocore
import newrelic.agent
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import current_app
import os

class SESMailer():

    def to_html(self, txt):
        html = '<html><body><p>' + txt.replace("\n", '</p><p>') + '</p></body></html>'
        return html

    def build_msg(self, **kwargs):
        recip_to = kwargs['to'] if 'to' in kwargs else None
        if not recip_to:
            raise('to required')
        recip_cc = kwargs['cc'] if 'cc' in kwargs else []
        recip_bcc = kwargs['bcc'] if 'bcc' in kwargs else []
        subject = kwargs['subject'] if 'subject' in kwargs else 'no subject'
        body = kwargs['body'] if 'body' in kwargs else 'this space left blank'
        attachments = kwargs['attach'] if 'attach' in kwargs else []

        msg = MIMEMultipart()
        msg['Subject'] = str(subject)
        msg['To'] = ', '.join(recip_to)
        msg['Cc'] = ', '.join(recip_cc)
        msg['Bcc'] = ', '.join(recip_bcc)
        msg['X-KSV-Sent-From'] = os.getenv('NEW_RELIC_APP_NAME', 'ksvotes-dev')

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

            # test our error handling
            if msg['To'] == current_app.config['FAIL_EMAIL']:
                raise RuntimeError('Failure testing works')

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
            newrelic.agent.record_exception()
            return {'msg': msg, 'MessageId': False, 'error': err}

        except (RuntimeError, TypeError, NameError) as err:
            current_app.logger.error(str(err))
            newrelic.agent.record_exception()
            return {'msg': msg, 'MessageId': False, 'error': err}

