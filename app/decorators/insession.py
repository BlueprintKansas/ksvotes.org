from functools import wraps
from flask import request, g, session as http_session, redirect, current_app
from app.models import Registrant
from uuid import UUID, uuid4

# check for session_id cookie, and corresponding Registrant db record.
# if can't find both, redirect to start page.
def InSession(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        def request_is_root():
            if request.path == '/' or request.url_rule.rule == '/<lang_code>/':
                return True
            return False

        session_id = http_session.get('session_id')
        g.registrant = None

        # if we don't yet have a session_id, assign one.
        if not session_id:
            uuid_str = str(uuid4())
            http_session['session_id'] = uuid_str
            current_app.logger.info("created session uuid %s" %(uuid_str))

            # edge case: a request "in the middle" of the flow.
            if not request_is_root():
                current_app.logger.info("redirect to flow start")
                return redirect('/') # TODO preserve lang_code?
        else:
            current_app.logger.info("found session uuid %s" %(session_id))
            g.registrant = Registrant.query.filter(Registrant.session_id == session_id).first()

        # edge case: clear stale cookie and start over.
        # adding in fix for index
        if session_id and not g.registrant and not request_is_root():
            current_app.logger.info('reset session')
            http_session.pop('session_id')
            return redirect('/') # TODO preserve lang_code?

        return f(*args, **kwargs)

    return decorated
