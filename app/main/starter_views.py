from app.main import main
from flask import g, url_for, render_template, jsonify, request, redirect, session as http_session, abort, current_app, flash
from flask_babel import lazy_gettext
import time
from app.main.forms import *
from app.models import Registrant, Clerk
from app import db
from uuid import UUID, uuid4
from app.decorators import InSession
from app.services import SessionManager
from app.services.steps import Step_0
from app.main.helpers import guess_locale

@main.route('/terms-of-service', methods=['GET'])
def terms():
    g.locale = guess_locale()
    return render_template('terms-of-service.html')

@main.route('/privacy-policy', methods=['GET'])
def privacy():
    g.locale = guess_locale()
    return render_template('privacy-policy.html')

#step 0 / 0x
@main.route('/', methods=["GET", "POST"])
@InSession
def index():
    registrant = g.get("registrant")
    form = FormStep0()
    if http_session.get('ref'):
        form = FormStep0(ref = http_session.get('ref'))
    elif request.cookies.get('ref'):
        form = FormStep0(ref = request.cookies.get('ref'))
    if registrant:
        form = FormStep0(
            ref = http_session.get('ref'),
            name_first = registrant.registration_value.get('name_first'),
            name_last = registrant.registration_value.get('name_last'),
            dob = registrant.registration_value.get('dob'),
            county = registrant.county,
            email = registrant.registration_value.get('email'),
            phone = registrant.registration_value.get('phone')
        )

    if request.method == "POST" and form.validate_on_submit():
        step = Step_0(form.data)
        if registrant:
            g.registrant.update(form.data)
        else:
            sid = UUID(http_session.get('session_id'), version=4)
            registrant = Registrant(
                county = form.data.get('county'),
                registration_value = form.data,
                session_id = sid,
                lang = g.lang_code,
            )
            db.session.add(registrant)

        step.run()
        registrant.reg_lookup_complete = step.reg_lookup_complete
        registrant.update({'sos_reg': list(map(lambda x: x['tree'], step.reg_found)) if step.reg_found else None})
        registrant.save(db.session)
        session_manager = SessionManager(registrant, step)
        return redirect(session_manager.get_redirect_url())

    else:
        return render_template('index.html', form=form)

@main.route('/change-or-apply/', methods=["GET"])
@InSession
def change_or_apply():
    sos_reg = g.registrant.try_value('sos_reg')
    county = g.registrant.county
    clerk = None
    if county:
        clerk = Clerk.find_by_county(county)

    return render_template('change-or-apply.html', sos_reg=sos_reg, clerk=clerk)

@main.route('/forget', methods=['GET', 'POST'])
def forget_session():
    g.locale = guess_locale()
    http_session['session_id'] = None
    flash(lazy_gettext('session_forgotten'), 'info')
    return redirect(url_for('main.index'))

# easy to remember
@main.route('/demo', methods=['GET'])
def demo_mode():
    return redirect('/ref?ref=demo')

@main.route('/ref', methods=['GET', 'POST'])
def referring_org():
    # we will accept whatever subset of step0 fields are provided.
    # we always start a new session, but we require a 'ref' code.
    if not request.values.get('ref'):
        return abort(404)

    sid = str(uuid4())

    # special 'ref' value of 'demo' attaches to the DEMO_UUID if defined
    if current_app.config['DEMO_UUID']:
        sid = current_app.config['DEMO_UUID']

    http_session['session_id'] = sid

    # if this is a GET request, make ref sticky via a cookie
    # and immediately redirect
    if request.method == 'GET':
        http_session['ref'] = request.values['ref']
        response = current_app.make_response(redirect(url_for('main.index')))
        response.set_cookie('ref', value=request.values['ref'])
        return response

    registration = {
        'name_last': request.values.get('name_last', ''),
        'name_first': request.values.get('name_first', ''),
        'dob': request.values.get('dob', ''),
        'email': request.values.get('email', ''),
        'phone': request.values.get('phone', ''),
    }
    registrant = Registrant(
        session_id = sid,
        county = request.values.get('county', ''),
        ref = request.values['ref'],
        registration_value = registration
    )
    db.session.add(registrant)
    db.session.commit()
    return redirect(url_for('main.index'))

