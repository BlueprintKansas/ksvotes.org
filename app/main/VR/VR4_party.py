from app.main import main
from flask import g, url_for, render_template, redirect, request
from app.main.forms import FormVR4
from app import db
from app.models import Registrant
from app.decorators import InSession
from app.services import SessionManager
from app.services.steps import Step_VR_4
@main.route('/vr/party', methods=["GET", "POST"])
@InSession
def vr4_party():
    form = FormVR4(
        party = g.registrant.party,
    )
    if request.method == "POST" and form.validate_on_submit():
        step = Step_VR_4(form.data)
        step.run()
        g.registrant.update(form.data)
        db.session.commit()
        session_manager = SessionManager(g.registrant,step)
        return redirect(session_manager.get_redirect_url())
    return render_template('vr/party.html', form=form)
