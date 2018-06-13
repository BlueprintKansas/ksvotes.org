from app.services.steps import Step

class Step_VR_3(Step):
	endpoint = '/vr/address'
    #this feels really redundant to me as the form should already require these to be in the payload before submitting.
	def is_complete(self):
		return False

	def next_step(self):
		return '/'
