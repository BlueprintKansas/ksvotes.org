from app.main import main
from flask import g, url_for, render_template, jsonify, request, redirect,session
import time
from app.main.forms import *
from app.models import Registrant
from app import db
from uuid import UUID, uuid4
from app.decorators import InSession
#step 0 / 0x

@main.route('/', methods=["GET", "POST"])
@InSession
def index():
    form = FormStep0()
    if request.method == "POST" and form.validate_on_submit():
        #get dict of data without the csrf_token
        form_data = form.data.pop('csrf_token', None)


        ## NEED registration check validation in here
        # do the ksvotesinfo lookup here.
        #

        ## if session id exists update data (assumption people hitting back button/navigating back to homepage)
        if g.get("registrant", None):
            #need to write update function that takes keys of new data and updates registration value
            g.registrant.update(data)
        ## create new registrant
        else:
            registrant = Registrant(
                registration_value = form_data,
                session_id = uuid4()
            )
            db.session.add(registrant)
            db.session.commit()
            ## set session id
            session['session_id'] = str(registrant.session_id)

        return redirect(url_for('main.change_or_apply'))

    return render_template('index.html', form=form)

@main.route('/change-or-apply', methods=["GET", "POST"])
@InSession
def change_or_apply():
    return render_template('change-or-apply.html')
