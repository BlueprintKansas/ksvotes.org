from app.main import main
from flask import g, url_for, render_template, redirect, request
from app import db
from app.models import Registrant
from app.decorators import InSession
from app.services import SessionManager
from app.main.forms import FormVR7
from app.main.VR.example_form import img_fill

@main.route('/vr/affirmation', methods=["GET", "POST"])
@InSession
def vr7_affirmation():
    registrant = g.registrant
    form = FormVR7()
    if request.method == "POST" and form.validate_on_submit():
        step = Step_VR_7(form.data)
        if step.run():
            g.registrant.update(form.data)
            db.session.commit()
            session_manager = SessionManager(g.registrant, step)
            return redirect(session_manager.get_redirect_url())

    return render_template('vr/affirmation.html', registrant=g.registrant, form=form)
