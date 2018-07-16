from app.services.steps import Step

class Step_AB_8(Step):
    endpoint = '/ab/submission'
    form_requirements = []
    step_requirements = []
    prev_step = 'Step_AB_7'
    next_step = None

    def run(self):
        if self.is_complete:
            return True

        if not self.verify_form_requirements():
            return False

        self.is_complete = True
        self.next_step = 'Step_1'
        return True
