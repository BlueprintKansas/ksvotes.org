from app.services.steps import Step

import os
import ksmyvoteinfo

class Step_0(Step):
    form_requirements = ['name_first', 'name_last', 'dob', 'email']
    step_requirements = ['reg_lookup_complete']
    reg_lookup_complete = False
    reg_found = False
    endpoint = '/'
    prev_step = None
    next_step = None

    def run(self):
        if self.is_complete:
            return True

        if not self.verify_form_requirements():
            return False

        self.reg_found = self.lookup_registration(
            name_first=self.form_payload['name_first'],
            name_last=self.form_payload['name_last'],
            dob=self.form_payload['dob'],
            county=self.form_payload['county']
        )
        self.is_complete = True
        self.reg_lookup_complete = True

        if self.reg_found:
            self.next_step = 'Step_1'
            return True

        self.next_step = 'Step_1'
        return True

    def lookup_registration(self, name_first, name_last, dob, county):
        if county == 'TEST':
            return False
        # any failure (exception) means we should try registering,
        # and leave it up to the counties to sort out dupes.
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
                county = county
            )
            if request:
                return request.parsed()
        except:
            return False

        return False
