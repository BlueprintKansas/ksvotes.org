import os

from app.services.steps import Step
from pyusps import address_information

class Step_VR_3(Step):
	form_requirements = ['addr', 'city', 'state', 'zip']
	step_requirements = ['addr_lookup_complete']
	address_order = ['current_address']
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


		validated_addresses = self.validate_addresses()



	def validate_addresses(self):
		"""
		Return values of usps lookup.  Keep track of order of addresses if multiple provided.
		"""
		#always expect the current address
		current_address = dict([
			('address', self.form_payload.get('addr', '')),
			 ('city', self.form_payload.get('city')),
			 ('state', self.form_payload.get('state')),
			 ('zip_code', self.form_payload.get('zip')),
			 ('address_extended', self.form_payload.get('unit'))
		])
		extra_addresses = []

		#construct additional addresses for request and update address_order
		if self.form_payload.get('has_prev_addr'):
			extra_addresses.append(dict([
			 ('address', self.form_payload.get('prev_addr', '')),
 		     ('city', self.form_payload.get('prev_city')),
	 	     ('state', self.form_payload.get('prev_state')),
	 		 ('zip_code', self.form_payload.get('prev_zip')),
	 	     ('address_extended', self.form_payload.get('prev_unit'))
			]))
			self.address_order.append('prev_addr')

		if self.form_payload.get('has_mail_addr'):
			extra_addresses.append(dict([
			 ('address', self.form_payload.get('mail_addr', '')),
 		     ('city', self.form_payload.get('mail_city')),
	 	     ('state', self.form_payload.get('mail_state')),
	 		 ('zip_code', self.form_payload.get('mail_zip')),
	 	     ('address_extended', self.form_payload.get('mail_unit'))
			]))
			self.address_order.append('prev_addr')

		if len(self.address_order) > 1:
			addrs = [current_address] + extra_addresses
			validated_addrs = address_information.verify(os.getenv('USPS_USER_ID'), *addrs)
			print(validated_addrs)
		else:
			return address_information.verify(os.getenv('USPS_USER_ID'), current_address)
