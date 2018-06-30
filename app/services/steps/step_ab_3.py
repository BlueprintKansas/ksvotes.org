from app.services.steps import Step
from flask import g

class Step_AB_3(Step):
    form_requirements = []
    step_requirements = []
    endpoint = '/ab/address'
    prev_step = 'Step_AB_1'
    next_step = None

    def run(self):
        if self.is_complete:
            return True

        if not self.verify_form_requirements():
            return False

        self.is_complete = True
        self.next_step = 'Step_AB_5'
        return True
