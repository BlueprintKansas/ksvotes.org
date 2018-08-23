from app.main import main
from flask import g, url_for, render_template, redirect, request, current_app
from app.main.forms import FormVR3
from app import db
from app.models import *
from app.decorators import InSession
from app.services import SessionManager
from app.services.steps import Step_VR_3

@main.route('/vr/address', methods=["GET", "POST"])
@InSession
def vr3_address():
    form = FormVR3(
        addr = g.registrant.registration_value.get('addr', ''),
        unit = g.registrant.registration_value.get('unit', ''),
        city = g.registrant.registration_value.get('city', ''),
        state = g.registrant.registration_value.get('state', 'KANSAS'),
        zip = g.registrant.registration_value.get('zip', ''),
        has_prev_addr = g.registrant.registration_value.get('has_prev_addr'),
        prev_addr = g.registrant.registration_value.get('prev_addr', ''),
        prev_unit = g.registrant.registration_value.get('prev_unit', ''),
        prev_city = g.registrant.registration_value.get('prev_city', ''),
        prev_state = g.registrant.registration_value.get('prev_state', ''),
        prev_zip = g.registrant.registration_value.get('prev_zip', ''),
        has_mail_addr = g.registrant.registration_value.get('has_mail_addr'),
        mail_addr = g.registrant.registration_value.get('mail_addr', ''),
        mail_unit = g.registrant.registration_value.get('mail_unit', ''),
        mail_city = g.registrant.registration_value.get('mail_city', ''),
        mail_state = g.registrant.registration_value.get('mail_state', ''),
        mail_zip = g.registrant.registration_value.get('mail_zip', ''),
    )
    if request.method == "POST" and form.validate_on_submit():
        step = Step_VR_3(form.data)
        step.run()
        update_data = form.data
        update_data['validated_addresses'] = step.validated_addresses
        g.registrant.update(update_data)
        g.registrant.addr_lookup_complete = step.addr_lookup_complete

        # override initial county guess with best guess based on validated address
        zip5 = g.registrant.best_zip5()
        county = ZIPCode.guess_county(zip5)
        current_app.logger.info("Lookup county %s based on ZIP5 %s" %(county, zip5))
        g.registrant.county = county

        db.session.commit()
        session_manager = SessionManager(g.registrant, step)
        return redirect(session_manager.get_redirect_url())
    return render_template('vr/address.html', form=form)
