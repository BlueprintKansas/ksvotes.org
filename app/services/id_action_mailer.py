from flask import current_app
from app.models import Clerk
from app.services.ses_mailer import SESMailer
from flask_babel import lazy_gettext
from jinja2 import Environment, FileSystemLoader
import os
import hashlib
import base64

class IdActionMailer():

  def __init__(self, registrant, clerk):
    self.ses = SESMailer()
    self.registrant = registrant
    self.clerk = clerk
    if self.clerk == None:
      raise Exception("No Clerk for County %s" %(registrant.county))
    self.env = Environment(loader=FileSystemLoader('%s/templates/' % current_app.root_path))
    self.set_subject()
    self.set_body()

  def subject_prefix(self):
    if os.getenv('EMAIL_PREFIX'):
      return os.getenv('EMAIL_PREFIX')
    else:
      return ''

  def set_subject(self):
    self.subject = self.subject_prefix() + lazy_gettext(u'voter_id_action_email_subject')

  def set_body(self):
    buf = lazy_gettext(u'voter_id_action_email_intro')
    buf += "\n"
    buf += lazy_gettext(u'voter_id_action_email_intro2')
    buf += " "
    buf += lazy_gettext(u'5AB_id_help')
    buf += "\n"
    buf += lazy_gettext(u'voter_id_action_email_instruction')
    template = self.env.get_template('clerk-details.html')
    buf += template.render(clerk=self.clerk).replace("\n", '')
    buf += "\n"
    buf += lazy_gettext(u'8VR_confirm_5')
    self.body = buf.format(firstname=self.registrant.try_value('name_first'))

  def send(self):
    reg_email = self.registrant.try_value('email')

    message = self.ses.build_msg(
      to=[reg_email],
      bcc=[],
      subject=self.subject,
      body=self.body
    )

    response = self.ses.send_msg(message, current_app.config['EMAIL_FROM'])
    current_app.logger.info("%s SENT ID Action needed %s" %(self.registrant.session_id, response))

    return response
