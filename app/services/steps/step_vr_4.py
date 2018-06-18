from app.services.steps import Step

class Step_VR_4(Step):
	form_requirements = ['party']
	step_requirements = []
	endpoint = '/vr/party'
	prev_step = 'Step_VR_3'
	next_step = None

	def run(self):
		if self.is_complete:
			return True

		if not self.verify_form_requirements():
			return False

		self.is_complete = True
		self.next_step = 'Step_VR_5'
		return True
