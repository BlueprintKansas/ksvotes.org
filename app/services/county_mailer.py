from flask import current_app
from app.models import Clerk
from app.services.ses_mailer import SESMailer
from flask_babel import lazy_gettext
import os
import hashlib
import base64

class CountyMailer():

    def __init__(self, registrant, clerk, form_img_type):
        self.ses = SESMailer()
        self.registrant = registrant
        self.form_imgs = registrant.try_value(form_img_type)
        if isinstance(self.form_imgs, str):
            self.form_imgs = [self.form_imgs]
        self.clerk = clerk
        if self.clerk == None:
            raise Exception("No Clerk for County %s" %(registrant.county))
        self.set_clerk_subject(form_img_type)
        self.set_receipt_subject(form_img_type)
        self.receipt_body = lazy_gettext(u'9_confirm_email').format(
            firstname=registrant.try_value('name_first'),
            county=self.clerk.county,
            officer=self.clerk.officer,
            email=self.clerk.email,
            phone=self.clerk.phone,
        )
        self.clerk_body = lazy_gettext(u'county_clerk_email')

    def set_clerk_subject(self, form_img_type):
        subject = 'No Subject'
        if form_img_type == 'ab_forms':
            subject = "New Advance Ballot application(s) for {}".format(self.registrant.name())
        elif form_img_type == 'vr_form':
            subject = "New Voter Registration for {}".format(self.registrant.name())
        else:
            raise Exception("Unknown form_img_type %s" %(form_img_type))

        self.clerk_subject = subject

    def set_receipt_subject(self, form_img_type):
        self.receipt_subject = lazy_gettext(u'voter_receipt_email_subject')

    def clerk_email(self):
        if self.clerk.county == 'TEST':
            return os.getenv('TEST_CLERK_EMAIL', self.clerk.email)
        elif os.getenv('TEST_CLERK_EMAIL'):
            return os.getenv('TEST_CLERK_EMAIL')
        else:
            return self.clerk.email

    def send(self):
        # we send 2 emails, and return dict of responses
        clerk_email = self.clerk_email()
        reg_email = self.registrant.try_value('email')

        if not clerk_email or not reg_email:
            current_app.logger.error("Missing clerk_email or reg_email for %s" %(self.registrant.session_id))
            return {}

        attachments = self.build_attachments()

        current_app.logger.info("%s SEND mail to %s" %(self.registrant.session_id, clerk_email))
        responses = {}

        # first is to clerk
        msg = self.ses.build_msg(
            attach=attachments,
            to=[clerk_email],
            cc=[reg_email],
            bcc=[current_app.config['EMAIL_BCC']],
            subject=self.clerk_subject,
            body=self.clerk_body,
        )
        responses['clerk'] = self.ses.send_msg(msg, current_app.config['EMAIL_FROM'])
        current_app.logger.info("%s SENT to clerk %s" %(self.registrant.session_id, responses['clerk']))

        # second is receipt to voter
        receipt = self.ses.build_msg(
            to=[reg_email],
            bcc=[],
            subject=self.receipt_subject,
            body=self.receipt_body,
        )
        responses['receipt'] = self.ses.send_msg(receipt, current_app.config['EMAIL_FROM'])
        current_app.logger.info("%s SENT receipt %s" %(self.registrant.session_id, responses['receipt']))

        return responses

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

