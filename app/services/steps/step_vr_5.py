from app.services.steps import Step

class Step_VR_5(Step):
    form_requirements = ['identification']
    step_requirements = []
    endpoint = '/vr/identification'
    prev_step = 'Step_VR_4'
    next_step = None

    def run(self):
        if self.is_complete:
            return True

        if not self.verify_form_requirements():
            return False

        self.is_complete = True
        self.next_step = 'Step_VR_6'
        return True
