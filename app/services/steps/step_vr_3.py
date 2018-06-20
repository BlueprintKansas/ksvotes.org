from app.services.steps import Step
from app.services.usps_api import USPS_API

class Step_VR_3(Step):
	form_requirements = ['addr', 'city', 'state', 'zip']
	step_requirements = ['addr_lookup_complete']
	address_order = ['current_address']
	addr_lookup_complete = False
	endpoint = '/vr/address'
	prev_step = 'Step_VR_2'
	next_step = None

	def run(self):
		if self.is_complete:
			return True

		if self.form_payload.get('has_prev_addr'):
			self.form_requirements = self.form_requirements + ['prev_addr', 'prev_city', 'prev_state', 'prev_zip']

		if self.form_payload.get('has_mail_addr'):
			self.form_requirements = self.form_requirements + ['mail_addr', 'mail_city', 'mail_state', 'mail_zip']

		if not self.verify_form_requirements():
			return False

		usps_api = USPS_API(self.form_payload)
		self.validated_addresses = usps_api.validate_addresses()
		self.next_step = 'Step_VR_4'
		self.addr_lookup_complete = True
		self.is_complete = True # always complete, regardless of USPS response. Invalid != incomplete
		return True
