from app.main import main
from flask import g, url_for, render_template, redirect, request, session as sess
from app import db
from app.main.forms import FormVR1
from app.models import Registrant
from app.decorators import InSession
from app.services import SessionManager
from app.services.steps import Step_VR_1

@main.route('/vr/citizenship', methods=["GET", "POST"])
@InSession
def vr1_citizenship():
    form = FormVR1()
    form = FormVR1(
        is_citizen = g.registrant.is_citizen
    )

    if request.method == "POST" and form.validate_on_submit():
        step = Step_VR_1(form.data)
        step.run()
        g.registrant.update(form.data)
        db.session.commit()
        session_manager = SessionManager(g.registrant, step)
        return redirect(session_manager.get_redirect_url())




    return render_template('vr/citizenship.html', form=form)
