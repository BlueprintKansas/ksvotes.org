from app.services.steps import Step

class Step_AB_5(Step):
    form_requirements = ['ab_identification']
    step_requirements = []
    endpoint = '/ab/identification'
    prev_step = 'Step_AB_3'
    next_step = None

    def run(self):
        if self.is_complete:
            return True

        if not self.verify_form_requirements():
            return False

        self.is_complete = True
        self.next_step = 'Step_AB_6'
        return True
