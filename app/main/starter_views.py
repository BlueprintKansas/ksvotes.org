from app.main import main
from flask import g, url_for, render_template, jsonify, request, redirect,session
import time
from app.main.forms import *
from app.models import Registrant
from app import db
from uuid import UUID, uuid4
from app.decorators import InSession
from app.services import Step_0
#step 0 / 0x

@main.route('/', methods=["GET", "POST"])
@InSession
def index():
    current_registrant = g.get("registrant")
    form = FormStep0()
    if current_registrant:
        form = FormStep0(
            name_first = current_registrant.registration_value.get('name_first'),
            name_last = current_registrant.registration_value.get('name_last'),
            dob = current_registrant.registration_value.get('dob'),
            county = current_registrant.registration_value.get('county'),
            email = current_registrant.registration_value.get('email'),
            phone = current_registrant.registration_value.get('phone')        
        )

    if request.method == "POST" and form.validate_on_submit():
        session_manager = Step_0(form.data)
        ## if session id exists update data (assumption people hitting back button/navigating back to homepage)
        if current_registrant:
            g.registrant.update(form.data)
            db.session.commit()
        ## create new registrant
        else:
            registrant = Registrant(
                registration_value = form.data,
                session_id = uuid4()
            )
            db.session.add(registrant)
            db.session.commit()
            ## set session id
            session['session_id'] = str(registrant.session_id)


        return redirect(session_manager.next_step())

    return render_template('index.html', form=form)

@main.route('/change-or-apply', methods=["GET", "POST"])
@InSession
def change_or_apply():
    return render_template('change-or-apply.html')
