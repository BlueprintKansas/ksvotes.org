from app.services.steps import Step

class Step_VR_1(Step):
	form_requirements = ['citizen']
	step_requirements = []
	endpoint = '/vr/citizenship'
	# prev_step = Step_0()
	next_step = None

	def all_requirements(self):
		return self.form_requirements + self.step_requirements

    #this feels really redundant to me as the form should already require these to be in the payload before submitting.
	def validate(self):
		if self.is_complete:
			return True
		if not all(k in self.form_payload for k in self.form_requirements):
			return False
		self.is_complete = True
		self.next_step = 'Step_VR_2'
