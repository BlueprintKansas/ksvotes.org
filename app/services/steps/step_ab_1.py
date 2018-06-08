from app.services.steps import Step

class Step_AB_1(Step):
	form_requirements = ['name_first', 'name_last', 'dob', 'county', 'email']
	step_requirements = ['reg_lookup_complete']

	def all_requirements(self):
		print(dir(self))
		return self.form_requirements + self.step_requirements
    #this feels really redundant to me as the form should already require these to be in the payload before submitting.
	def is_complete(self):
		return False

	def next_step(self):
		return '/'
