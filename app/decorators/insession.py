from functools import wraps
from flask import request, g, session as http_session, redirect, current_app, url_for, flash
from flask_babel import lazy_gettext
from app.models import Registrant
from uuid import UUID, uuid4
from app.main.helpers import guess_locale

# check for session_id cookie, and corresponding Registrant db record.
# if can't find both, redirect to start page.
def InSession(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        def request_is_root():
            if request.path == '/' or request.url_rule.rule == '/<lang_code>/':
                return True
            return False

        http_session.permanent = True # enforce expiration TTL
        session_id = http_session.get('session_id')
        g.registrant = None
        g.locale = guess_locale() # so we have it available for all template rendering

        # if we don't yet have a session_id, assign one.
        if not session_id:
            current_app.logger.debug("No session_id found")
            uuid_str = str(uuid4())
            http_session['session_id'] = uuid_str
            current_app.logger.debug("created session uuid %s" %(uuid_str))

            # edge case: a request "in the middle" of the flow.
            if not request_is_root():
                current_app.logger.error("redirect to flow start")
                if request.method == 'POST':
                    flash(lazy_gettext('session_interrupted_error'), 'warning')
                return redirect(url_for('main.index'))
        else:
            current_app.logger.debug("found session uuid %s" %(session_id))
            g.registrant = Registrant.find_by_session(session_id)
            # Security belt-and-suspenders. Disallow session continuation if the Registrant
            # has not been updated within the SESSION_TTL window.
            r = g.registrant
            if r and not r.updated_since(current_app.config['SESSION_TTL']) and not r.is_demo():
                current_app.logger.error("Discontinuing old session for existing Registrant.")
                http_session['session_id'] = None
                if request.method == 'POST':
                    flash(lazy_gettext('session_interrupted_error'), 'warning')
                return redirect(url_for('main.index'))

        # edge case: clear stale cookie and start over.
        # adding in fix for index
        if session_id and not g.registrant and not request_is_root():
            current_app.logger.debug('reset session')
            http_session.pop('session_id')
            return redirect(url_for('main.index'))

        return f(*args, **kwargs)

    return decorated
