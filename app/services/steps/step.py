
class Step():
	def __init__(self, form_payload = None):
		self.form_payload = form_payload
	is_complete = False
	next_step = None
	prev_step = None
	endpoint = None
	form_requirements = []
	step_requirements = []

	def all_requirements(self):
		return self.form_requirements + self.step_requirements
