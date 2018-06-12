from app.services.steps import Step

class Step_VR_2(Step):
	endpoint = '/vr/name'

    #this feels really redundant to me as the form should already require these to be in the payload before submitting.
	def is_complete(self):
		return False

	def next_step(self):
		return '/'
