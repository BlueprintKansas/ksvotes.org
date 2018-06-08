from app.services.steps import *

class SessionManager():
    def __init__(self, registrant, current_step):
        self.registrant = registrant
        self.current_step = current_step

    def get_next(self):
        if not self.current_step.prev_step and self.current_step.is_complete:
            return self.current_step.next_step
        prev_step = getattr(module, self.current_step.prev_step)
        return self.verify_prev_step(prev_step)

    def verify_prev_step(self, step):
        for req in step.all_requirements():
            if req in self.registrant.__table__.columns:
                if not getattr(self.registrant, req):
                    return self.current_step.prev_step.endpoint
            else:
                if not self.registrant.registration_value.get(req):
                    return self.current_step.prev_step.endpoint
        return self.current_step.next_step
