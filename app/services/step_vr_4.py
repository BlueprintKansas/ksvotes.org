from app.services import Step

class Step_VR_4(Step):

    #this feels really redundant to me as the form should already require these to be in the payload before submitting.
	def is_complete(self):
		return False

	def next_step(self):
		return '/'
