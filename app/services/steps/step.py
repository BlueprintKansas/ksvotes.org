
class Step():
    def __init__(self, form_payload = None):
        self.form_payload = form_payload
    is_complete = False
    next_step = None
    prev_step = None
    endpoint = None
    form_requirements = []
    step_requirements = []

    def all_requirements(self):
        return self.form_requirements + self.step_requirements

    #verify that all model points are met
    def verify_form_requirements(self):
        if not all(k in self.form_payload for k in self.form_requirements):
            return False
        return True
