from app.services import Step
import ksmyvoteinfo

class Step_0(Step):

	def lookup_registration(self, name_first, name_last, dob, county):
		kmvi = ksmyvoteinfo.KsMyVoteInfo()
		dob = dob.split('/')
		formatted_dob = "{year}-{month}-{day}".format(year=dob[2], month=dob[0], day=dob[1])
		request = kmvi.lookup(
						first_name=name_first,
						last_name=name_last,
						dob = formatted_dob,
						county=county
				)
		if request:
			return request
		else:
			return False

    #this feels really redundant to me as the form should already require these to be in the payload before submitting.
	def is_complete(self):
		s0_requirements = ['name_first', 'name_last', 'dob', 'email', 'county']
		if all(k in self.form_payload for k in s0_requirements):
			return True
		return False

	def next_step(self):
		if self.is_complete() and self.lookup_registration(name_first=self.form_payload['name_first'], name_last=self.form_payload['name_last'], dob=self.form_payload['dob'], county=self.form_payload['county']):
			return '/change-or-apply'
		elif self.is_complete():
			return '/vr/citizenship'
		else:
			return '/'
