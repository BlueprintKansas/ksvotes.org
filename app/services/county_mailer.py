from flask import g, current_app
from app.models import Clerk

class CountyMailer():

    def __init__(self, registrant, form_img):
        self.registrant = registrant
        self.form_img = form_img
        self.clerk = Clerk.find_by_county(registrant.county)
        if self.clerk == None:
            raise Exception("No Clerk for County %s" %(registrant.county))

    def send(self):
        current_app.logger.info("SEND mail to %s, %s" %(self.clerk.email, self.registrant.try_value('email')))
        return True # TODO
