from app.services.steps import Step

class Step_VR_7(Step):
    endpoint = '/vr/affirmation'
    form_requirements = ['affirmation']
    step_requirements = []
    prev_step = 'Step_VR_6'
    next_step = None

    def run(self):
        if self.is_complete:
            return True

        if not self.verify_form_requirements():
            return False

        self.is_complete = True
        self.next_step = 'Step_VR_8'
        return True
