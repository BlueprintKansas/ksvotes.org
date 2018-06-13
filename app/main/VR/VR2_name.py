from app.main import main
from flask import g, url_for, render_template, redirect, request
from app.main.forms import FormVR2
from app.models import Registrant
from app import db
from app.decorators import InSession
from app.services import SessionManager
from app.services.steps import Step_VR_2

@main.route('/vr/name', methods=["GET", "POST"])
@InSession
def vr2_name():
    form = FormVR2(
        prefix = g.registrant.registration_value.get('prefix', ''),
        name_first = g.registrant.registration_value.get('name_first', ''),
        name_middle = g.registrant.registration_value.get('name_middle', ''),
        name_last = g.registrant.registration_value.get('name_last', ''),
        suffix = g.registrant.registration_value.get('suffix', ''),
        has_prev_name = g.registrant.registration_value.get('has_prev_name', ''),
        prev_prefix = g.registrant.registration_value.get('prev_prefix', ''),
        prev_name_first = g.registrant.registration_value.get('prev_name_first', ''),
        prev_name_middle = g.registrant.registration_value.get('prev_name_middle', ''),
        prev_name_last = g.registrant.registration_value.get('prev_name_last', ''),
        prev_suffix = g.registrant.registration_value.get('prev_suffix', ''),
    )
    if request.method == "POST" and form.validate_on_submit():
        step = Step_VR_2(form.data)
        step.run()
        g.registrant.update(form.data)
        db.session.commit()
        session_manager = SessionManager(g.registrant,step)
        return redirect(session_manager.get_redirect_url())
    return render_template('vr/name.html', form=form)
