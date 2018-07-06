from app.services.steps import Step
from flask import g
from app.services.usps_api import USPS_API

class Step_AB_3(Step):
    form_requirements = ['addr', 'city', 'state', 'zip']
    step_requirements = ['addr_lookup_complete']
    address_order = ['current_address']
    endpoint = '/ab/address'
    addr_lookup_complete = False
    prev_step = 'Step_AB_1'
    next_step = None

    def run(self):
        if self.is_complete:
            return True

        if self.form_payload.get('has_mail_addr'):
            self.form_requirements = self.form_requirements + ['mail_addr', 'mail_city', 'mail_state', 'mail_zip']

        if not self.verify_form_requirements():
            return False

        usps_api = USPS_API(self.form_payload)
        self.validated_addresses = usps_api.validate_addresses()
        self.addr_lookup_complete = True
        self.is_complete = True
        self.next_step = 'Step_AB_5'
        return True
