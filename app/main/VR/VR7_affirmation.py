from app.main import main
from flask import g, url_for, render_template, redirect, request
from app import db
from app.models import Registrant
from app.decorators import InSession
from app.services import SessionManager
from app.services.nvris_client import NVRISClient
from app.services.county_mailer import CountyMailer
from app.services.steps import Step_VR_7
from app.main.forms import FormVR7

@main.route('/vr/affirmation', methods=["GET", "POST"])
@InSession
def vr7_affirmation():
    registrant = g.registrant
    form = FormVR7()
    if request.method == "POST" and form.validate_on_submit():
        step = Step_VR_7(form.data)
        if step.run():
            g.registrant.update(form.data)
            nvris_client = NVRISClient(g.registrant)
            vr_form = nvris_client.get_vr_form()
            if vr_form:
                g.registrant.last_completed_step = 7
                g.registrant.update({ 'vr_form': vr_form })
                db.session.commit()
                mailer = CountyMailer(g.registrant, vr_form)
                mailer.send()
            else:
                step.is_complete = False

            session_manager = SessionManager(g.registrant, step)
            return redirect(session_manager.get_redirect_url())

    # TODO worry about DDoS if we preview on every GET?
    nvris_client = NVRISClient(g.registrant)
    preview_img = nvris_client.get_vr_form()
    return render_template('vr/affirmation.html', preview_img=preview_img, registrant=g.registrant, form=form)
