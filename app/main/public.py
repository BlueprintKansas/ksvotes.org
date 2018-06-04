from app.main import main
from flask import g, url_for, render_template, jsonify, request, redirect,session
import time
from app.main.forms import *
from app.models import Registrant
from app import db
from uuid import UUID, uuid4
from app.decorators import SessionManager
#step 0 / 0x

@main.route('/', methods=["GET", "POST"])
@SessionManager
def index():
    form = FormStep0()
    next_step = url_for('main.citizenship')
    if request.method == "POST" and form.validate_on_submit():
        #get dict of data without the csrf_token
        data = form.data.pop('csrf_token', None)


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
                registration_value = form.data,
                session_id = uuid4()
            )
            db.session.add(registrant)
            db.session.commit()
            ## set session id
            session['session_id'] = str(registrant.session_id)

        return redirect(url_for('main.citizenship'))

    return render_template('index.html', form=form)

#step 1
@main.route('/citizenship', methods=["GET", "POST"])
@SessionManager
def citizenship():
    print(session)
    print(g.registrant.registration_value.get('name_first'))
    form = FormVR1()
    if request.method == "POST" and form.validate_on_submit():
        return jsonify({"post": "success"})

    return render_template('citizenship.html', form=form)

#step 2
@main.route('/name', methods=["GET", "POST"])
def name():
    form = FormVR2()
    if request.method == "POST" and form.validate_on_submit():
        return jsonify({"post": "success"})
    return render_template('name.html', form=form)

#step 3
@main.route('/address', methods=["GET", "POST"])
def address():
    form = FormVR3()
    if request.method == "POST" and form.validate_on_submit():
        return jsonify({"post": "success"})
    return render_template('address.html', form=form)

#step 4
@main.route('/party', methods=["GET", "POST"])
def party():
    form = FormVR4()
    if request.method == "POST" and form.validate_on_submit():
        return jsonify({"post": "success"})
    return render_template('party.html', form=form)

#step 5 (4? 4.5?)
@main.route('/identification', methods=["GET", "POST"])
def identification():
    form = FormVR5()
    if request.method == "POST" and form.validate_on_submit():
        return jsonify({"post": "success"})
    return render_template('identification.html', form=form)

#step 6 NVRIS preview
@main.route('/preview')
def preview():
    # include signing box
    return 'preview'

#step 7 (affirm signature) (redirect if desktop?)
@main.route('/affirmation')
def affirmation():
    return "affirmation"

#step 8 confirmation reciept and next steps (share?)
@main.route('/confirmation')
def confirmation():
    return 'confirmation'
