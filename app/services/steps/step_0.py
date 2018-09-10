from app.services.steps import Step
from app.models import ZIPCode
from flask import current_app
import os
import sys
import ksmyvoteinfo
import requests

class Step_0(Step):
    form_requirements = ['name_first', 'name_last', 'dob', 'email']
    step_requirements = ['reg_lookup_complete']
    reg_lookup_complete = False
    reg_found = False
    voter_view_fail = False
    endpoint = '/'
    prev_step = None
    next_step = None

    def run(self, skip_sos=False):
        if self.is_complete:
            return True

        if not self.verify_form_requirements():
            return False

        if not skip_sos:
            self.reg_found = self.lookup_registration(
                name_first=self.form_payload['name_first'],
                name_last=self.form_payload['name_last'],
                dob=self.form_payload['dob'],
            )

        self.is_complete = True
        self.reg_lookup_complete = True

        if self.reg_found:
            self.next_step = 'Step_1'
            return True

        self.next_step = 'Step_1'
        return True

    def lookup_registration(self, name_first, name_last, dob):
        try:
            kmvi = ksmyvoteinfo.KsMyVoteInfo()
            if os.getenv('VOTER_VIEW_URL'):
                kmvi = ksmyvoteinfo.KsMyVoteInfo(url=os.getenv('VOTER_VIEW_URL'))
            dob = dob.split('/')
            formatted_dob = "{year}-{month}-{day}".format(year=dob[2], month=dob[0], day=dob[1])
            request = kmvi.lookup(
                first_name = name_first,
                last_name = name_last,
                dob = formatted_dob,
            )
            if request:
                return request.parsed()
        except requests.exceptions.ConnectionError as err:
            self.voter_view_fail = kmvi.url
            current_app.logger.warn("voter view connection failure: %s" %(err))
            return False
        except:
            err = sys.exc_info()[0]
            current_app.logger.warn("voter view failure: %s" %(err))
            return False

        return False
