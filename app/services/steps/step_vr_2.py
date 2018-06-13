from app.services.steps import Step

class Step_VR_2(Step):
	form_requirements = ['name_first', 'name_last']
	step_requirements = []
	endpoint = '/vr/name'
	prev_step = 'Step_VR_1'
	next_step = None

	def run(self):
		if self.is_complete:
			return True

		if not self.verify_form_requirements():
			return False

		self.is_complete = True
		self.next_step = 'Step_VR_3'
		return True
