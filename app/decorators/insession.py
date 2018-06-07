from functools import wraps
from flask import request, g, session
from app.models import Registrant
from uuid import UUID


def InSession(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        session_id = session.get('session_id')
        if session_id:
            try:
                sid = UUID(session_id, version=4)
                registrant = Registrant.query.filter(Registrant.session_id == sid).first()
                if registrant:
                    #set request global to current registrant
                    g.registrant = registrant
                else:
                    #delete invalid registration uuid
                    session.pop('session_id')
            except:
                #if not valid uuid session_id delete
                session.pop('session_id')
        return f(*args, **kwargs)
    return decorated
