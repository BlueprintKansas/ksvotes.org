
class Step():
    def __init__(self, form_payload = None):
        self.form_payload = form_payload

    def is_complete(self):
        return False

    def next_step(self):
        return '/'

    def prev_step(self):
        return '/'
        
