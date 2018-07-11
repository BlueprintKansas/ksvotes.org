from app.main import main
from flask import g, url_for, render_template, redirect, request
from app import db
from app.models import Registrant
from app.decorators import InSession
from app.services import SessionManager
from app.services.nvris_client import NVRISClient
from app.main.forms import FormVR6
from app.main.VR.example_form import img_fill
from app.services.steps import Step_VR_6

@main.route('/vr/preview', methods=["GET", "POST"])
@InSession
def vr6_preview_sign():
    form = FormVR6(
        signature_string = g.registrant.try_value('signature_string')
    )
    if request.method == "POST" and form.validate_on_submit():
        step = Step_VR_6(form.data)
        if step.run():
            g.registrant.update(form.data)
            db.session.commit()
            session_manager = SessionManager(g.registrant, step)
            return redirect(session_manager.get_redirect_url())

    # TODO worry about DDoS if we preview on every GET?
    nvris_client = NVRISClient(g.registrant)
    preview_img = nvris_client.get_vr_form()
    return render_template('vr/preview-sign.html', preview_img=preview_img, registrant=g.registrant, form=form)
