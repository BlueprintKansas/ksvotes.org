from app.services.steps import *

class SessionManager():
    """
    Session manager is responsible for taking in a registrant and current step and then determining which step needs to be performed next.

    """
    # initialize these as None, override them with init method if valid.
    next_step = None
    prev_step = None

    def __init__(self, registrant, current_step):
        self.registrant = registrant
        self.current_step = current_step
        self._init_next_step()
        self._init_prev_step()

    def _init_next_step(self):
        """
        If the current step has a next step set, initialize the next step class and save it to self.
        """
        if self.current_step.next_step:
            next_step = globals()[self.current_step.next_step]
            self.next_step = next_step()

    def _init_prev_step(self):
        """
        If the current step has a previous step set, initialize the previous step class and save it to self.
        """
        if self.current_step.prev_step:
            prev_step = globals()[self.current_step.prev_step]
            self.prev_step = prev_step()

    def get_redirect_url(self):
        """
        Should always return a url path.  Look at the current step and determine if the user needs to:
            A: Move on to next step.
            B: Move back to previous step.
            C: Stay at current step.
        """
        # For Step 0 when no previous step exists
        if not self.prev_step:
            if self.current_step.is_complete:
                return self.next_step.endpoint
            else:
                # could use some error message logic here... but a user shouldn't ever get here (famous last words)
                return self.current_step.endpoint

        # For the previous step iterate all of the requirements.
        # If the requirement is not fulfilled return the previous step url
        for req in self.prev_step.all_requirements():
            # if a requirement is missing return the endpoint for the previous step
            if not self.registrant.has_value_for_req(req):
                return self.prev_step.endpoint

        # if the step has been completed move on
        if self.current_step.is_complete:
            return self.next_step.endpoint

        #default to returning current step
        return self.current_step.endpoint


    # def check_value_of_requirement(req):
    #     """
    #     For each requirement determine if it is a column in the database table otherwise look for an object in the registration_value string.
    #     If the registrant has no value stored for a requirement return false.
    #     """
    #     if req in self.registrant.__table__.columns:
    #         if not getattr(self.registrant, req):
    #             return False
    #     else:
    #         if not self.registrant.registration_value.get(req):
    #             return False
    #     return True
