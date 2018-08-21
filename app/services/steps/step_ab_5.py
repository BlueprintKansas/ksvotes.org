from app.services.steps import Step

class Step_AB_5(Step):
    form_requirements = []
    step_requirements = []
    endpoint = '/ab/identification'
    prev_step = 'Step_AB_3'
    next_step = None

    def run(self):
        if self.is_complete:
            return True

        if not self.verify_form_requirements():
            return False

        if not self.valid_id():
            return False

        self.is_complete = True
        self.next_step = 'Step_AB_6'
        return True

    def valid_id(self):
        from app.main.helpers import KS_DL_PATTERN
        import re

        k = 'ab_identification'

        # it's ok if k is None but if present must match pattern.

        if not self.form_payload:
            return True
        if k not in self.form_payload:
            return True
        ab_id = self.form_payload[k]
        if ab_id == '':
            return True
        if re.match(KS_DL_PATTERN, ab_id):
            return True
        return False
           
