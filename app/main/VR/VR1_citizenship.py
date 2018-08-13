from app.main import main
from flask import g, url_for, render_template, redirect, request
from app import db
from app.main.forms import FormVR1
from app.models import Registrant
from app.decorators import InSession
from app.services import SessionManager
from app.services.steps import Step_VR_1

@main.route('/vr/citizenship', methods=["GET", "POST"])
@InSession
def vr1_citizenship():
    reg = g.registrant
    form = FormVR1(
        is_citizen = reg.is_citizen,
        is_eighteen = reg.is_eighteen,
    )

    if request.method == "POST" and form.validate_on_submit():
        step = Step_VR_1(form.data)
        if step.run():
            reg.update(form.data)
            reg.last_completed_step = 1
            reg.save(db.session)
            session_manager = SessionManager(reg, step)
            return redirect(session_manager.get_redirect_url())

    return render_template('vr/citizenship.html', form=form)
