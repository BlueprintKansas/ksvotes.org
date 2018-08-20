from app.main import main
from flask import g, url_for, render_template, redirect, request
from flask_babel import lazy_gettext
from app import db
from app.models import Registrant, Clerk
from app.decorators import InSession
from app.services import SessionManager
from app.services.nvris_client import NVRISClient
from app.services.county_mailer import CountyMailer
from app.services.steps import Step_VR_7
from app.main.forms import FormVR7
from datetime import datetime

@main.route('/vr/affirmation', methods=["GET", "POST"])
@InSession
def vr7_affirmation():
    reg = g.registrant
    clerk = reg.try_clerk()
    form = FormVR7()

    # if we don't have a VR form to affirm, redirect to Step 0
    if not reg.try_value('vr_form', False):
        return redirect(url_for('main.index'))

    vr_form = reg.try_value('vr_form')

    if request.method == "POST" and form.validate_on_submit():
        step = Step_VR_7(form.data)
        if step.run():
            # TODO we don't want County, just Affirmation
            # and that must always be true on a POST, so just hardcode it.
            # if we ever expand the Form fields, we'll need to revisit.
            reg.update({'affirmation': True})
            reg.vr_completed_at = datetime.utcnow()
            reg.save(db.session)

            mailer = CountyMailer(reg, clerk, 'vr_form')
            r = mailer.send()

            # any error gets a special page
            for k in ['clerk', 'receipt']:
                if k not in r or 'MessageId' not in r[k] or not r[k]['MessageId']:
                    # TODO log New Relic event
                    return render_template('email_error.html', clerk=clerk)

            reg.update({'vr_form_message_id': r['clerk']['MessageId']})
            reg.save(db.session)

            session_manager = SessionManager(reg, step)
            return redirect(session_manager.get_redirect_url())

    return render_template('vr/affirmation.html', clerk=clerk, preview_img=vr_form, form=form)
