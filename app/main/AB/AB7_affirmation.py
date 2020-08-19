from app.main import main
from flask import g, url_for, render_template, redirect, request
from flask_babel import lazy_gettext
from app import db
from app.models import Registrant, Clerk
from app.decorators import InSession
from app.services import SessionManager
from app.services.nvris_client import NVRISClient
from app.services.county_mailer import CountyMailer
from app.services.id_action_mailer import IdActionMailer
from app.services.steps import Step_AB_7
from app.main.forms import FormAB7, CountyPicker
from datetime import datetime

@main.route('/ab/affirmation', methods=["GET", "POST"])
@InSession
def ab7_affirmation():
    reg = g.registrant
    form = FormAB7()
    clerk = reg.try_clerk()
    county_picker = CountyPicker()

    # if we don't have a signed AB form to affirm, redirect
    if not reg.try_value('ab_forms', False):
        if not reg.try_value('signature_string', False):
            return redirect(url_for('main.index'))
        else:
            return redirect(url_for('main.ab6_preview_sign'))

    ab_forms = reg.try_value('ab_forms')

    if request.method == "POST" and form.validate_on_submit():
        step = Step_AB_7(form.data)
        if step.run():
            reg.update(form.data)
            reg.save(db.session)

            mailer = CountyMailer(reg, clerk, 'ab_forms')
            r = mailer.send()

            # if there was no ID string defined, send the action-needed email
            if not reg.ab_permanent and not reg.try_value('ab_identification'):
                id_action_mailer = IdActionMailer(reg, clerk)
                resp = id_action_mailer.send()
                reg.update({'ab_id_action_email_sent': resp['MessageId']})

            # any error gets a special page
            for k in ['clerk', 'receipt']:
                if k not in r or 'MessageId' not in r[k] or not r[k]['MessageId']:
                    # TODO log New Relic event
                    return render_template('email_error.html', clerk=clerk)

            reg.update({'ab_forms_message_id': r['clerk']['MessageId']})
            reg.ab_completed_at = datetime.utcnow()
            reg.save(db.session)

            session_manager = SessionManager(reg, step)
            return redirect(session_manager.get_redirect_url())

    return render_template('ab/affirmation.html', preview_imgs=ab_forms, form=form, clerk=clerk, county_picker=county_picker)
