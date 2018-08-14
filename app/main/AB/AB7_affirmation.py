from app.main import main
from flask import g, url_for, render_template, redirect, request
from flask_babel import lazy_gettext
from app import db
from app.models import Registrant, Clerk
from app.decorators import InSession
from app.services import SessionManager
from app.services.nvris_client import NVRISClient
from app.services.county_mailer import CountyMailer
from app.services.steps import Step_AB_7
from app.main.forms import FormAB7

@main.route('/ab/affirmation', methods=["GET", "POST"])
@InSession
def ab7_affirmation():
    reg = g.registrant
    form = FormAB7()
    clerk = Clerk.find_by_county(reg.county)

    # if we don't have a AB form to affirm, redirect to Step 0
    if not reg.try_value('ab_forms', False):
        return redirect(url_for('main.index'))

    ab_forms = reg.try_value('ab_forms')

    if request.method == "POST" and form.validate_on_submit():
        step = Step_AB_7(form.data)
        if step.run():
            # TODO we don't want County, just Affirmation
            # and that must always be true on a POST, so just hardcode it.
            # if we ever expand the Form fields, we'll need to revisit.
            reg.update({'affirmation': True})
            reg.last_completed_step = 7
            reg.save(db.session)

            mailer = CountyMailer(reg, clerk, 'ab_forms')
            r = mailer.send()

            # any error gets a special page
            for k in ['clerk', 'receipt']:
                if k not in r or 'MessageId' not in r[k] or not r[k]['MessageId']:
                    # TODO log New Relic event
                    return render_template('email_error.html', clerk=clerk)

            reg.update({'ab_forms_message_id': r['clerk']['MessageId']})
            reg.save(db.session)

            session_manager = SessionManager(reg, step)
            return redirect(session_manager.get_redirect_url())

    return render_template('ab/affirmation.html', preview_imgs=ab_forms, form=form, clerk=clerk)
