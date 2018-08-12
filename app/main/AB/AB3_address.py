from app.main import main
from flask import g, url_for, render_template, redirect, request, current_app
from app.main.forms import FormAB3
from app.decorators import InSession
from app.services.steps import Step_AB_3
from app import db
from app.services import SessionManager
from app.models import *

@main.route('/ab/address', methods=["GET", "POST"])
@InSession
def ab3_address():
    form = FormAB3(
        addr = g.registrant.try_value('addr'),
        unit = g.registrant.try_value('unit'),
        city = g.registrant.try_value('city'),
        state = g.registrant.try_value('state', 'KANSAS'),
        zip = g.registrant.try_value('zip'),
        has_mail_addr = g.registrant.try_value('has_mail_addr'),
        mail_addr = g.registrant.try_value('mail_addr'),
        mail_unit = g.registrant.try_value('mail_unit'),
        mail_city = g.registrant.try_value('mail_city'),
        mail_state = g.registrant.try_value('mail_state'),
        mail_zip = g.registrant.try_value('mail_zip'),
    )
    if request.method == "POST" and form.validate_on_submit():
        step = Step_AB_3(form.data)
        if step.run():
            update_data = form.data
            update_data['validated_addresses'] = step.validated_addresses
            g.registrant.update(update_data)
            g.registrant.addr_lookup_complete = step.addr_lookup_complete

            # guess county based on ZIP if necessary.
            if not g.registrant.county or len(g.registrant.county) == 0:
                zip5 = g.registrant.try_value('zip')
                county = ZIPCode.guess_county(zip5)
                current_app.logger.info("Lookup county %s based on ZIP5 %s" %(county, zip5))
                g.registrant.county = county

            db.session.commit()
            session_manager = SessionManager(g.registrant, step)
            return redirect(session_manager.get_redirect_url())
    
    return render_template('/ab/address.html', form=form)
