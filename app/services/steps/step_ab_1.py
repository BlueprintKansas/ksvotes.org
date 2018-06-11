from app.services.steps import Step

class Step_AB_1(Step):
	endpoint = '/change-or-apply'
	prev_step = 'Step_0'
	next_step = None
