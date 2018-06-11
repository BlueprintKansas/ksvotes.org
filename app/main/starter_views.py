from app.main import main
from flask import g, url_for, render_template, jsonify, request, redirect,session
import time
from app.main.forms import *
from app.models import Registrant
from app import db
from uuid import UUID, uuid4
from app.decorators import InSession
from app.services import SessionManager
from app.services.steps import Step_0
#step 0 / 0x

@main.route('/', methods=["GET", "POST"])
@InSession
def index():
    registrant = g.get("registrant")
    form = FormStep0()
    if registrant:
        form = FormStep0(
            name_first = registrant.registration_value.get('name_first'),
            name_last = registrant.registration_value.get('name_last'),
            dob = registrant.registration_value.get('dob'),
            county = registrant.registration_value.get('county'),
            email = registrant.registration_value.get('email'),
            phone = registrant.registration_value.get('phone')
        )

    if request.method == "POST" and form.validate_on_submit():
        step = Step_0(form.data)
        if registrant:
            g.registrant.update(form.data)
        else:
            registrant = Registrant(
                county = form.data.get('county'),
                registration_value = form.data,
                session_id = uuid4()
            )
            db.session.add(registrant)
            session['session_id'] = str(registrant.session_id)

        #run step
        step.run()
        #update any non form variables/non
        registrant.reg_lookup_complete = step.reg_lookup_complete
        db.session.commit()

        session_manager = SessionManager(registrant, step)
        return redirect(session_manager.get_redirect_url())

    return render_template('index.html', form=form)

@main.route('/change-or-apply', methods=["GET", "POST"])
@InSession
def change_or_apply():
    return render_template('change-or-apply.html')
