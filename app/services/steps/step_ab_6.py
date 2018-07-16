from app.services.steps import Step

class Step_AB_6(Step):
    endpoint = '/ab/preview'
    form_requirements = ['signature_string']
    step_requirements = []
    prev_step = 'Step_AB_5'
    next_step = None

    def run(self):
        if self.is_complete:
            return True

        if not self.verify_form_requirements():
            return False

        self.is_complete = True
        self.next_step = 'Step_AB_7'
        return True
