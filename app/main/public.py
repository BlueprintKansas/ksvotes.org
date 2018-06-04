from app.main import main
from flask import g, url_for, render_template, jsonify, request, redirect
import time
from app.main.forms import *
#step 0 / 0x


@main.route('/', methods=["GET", "POST"])
def index():
    form = FormStep0()
    if request.method == "POST" and form.validate_on_submit():
        return jsonify({"post": "success"})

    return render_template('index.html', form=form)

#step 1
@main.route('/citizenship', methods=["GET", "POST"])
def citizenship():
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
