
class Step():
    def __init__(self, form_payload = None):
        self.form_payload = form_payload
    is_complete = False
    next_step = None
    prev_step = None
    endpoint = None
