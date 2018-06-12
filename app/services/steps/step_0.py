from app.services.steps import Step

import ksmyvoteinfo

class Step_0(Step):
	form_requirements = ['name_first', 'name_last', 'dob', 'county', 'email']
	step_requirements = ['reg_lookup_complete']
	reg_lookup_complete = False
	endpoint = '/'
	prev_step = None
	next_step = None

	def run(self):
		if self.is_complete:
			return True

		## verify all model points are met
		# if not all(k in self.form_payload for k in self.form_requirements):
		# 	return False
		if not self.verify_form_requirements():
			return False

		
		reg_lookup = self.lookup_registration(name_first=self.form_payload['name_first'], name_last=self.form_payload['name_last'], dob=self.form_payload['dob'], county=self.form_payload['county'])
		self.is_complete = True
		self.reg_lookup_complete = True

		if reg_lookup:
			self.next_step = 'Step_AB_1'
			return True

		self.next_step = 'Step_VR_1'
		return True

	def lookup_registration(self, name_first, name_last, dob, county):
		kmvi = ksmyvoteinfo.KsMyVoteInfo()
		dob = dob.split('/')
		formatted_dob = "{year}-{month}-{day}".format(year=dob[2], month=dob[0], day=dob[1])
		request = kmvi.lookup(
						first_name = name_first,
						last_name = name_last,
						dob = formatted_dob,
						county = county
				)
		if request:
			return request

		return False
