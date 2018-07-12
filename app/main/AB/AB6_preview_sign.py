from app.main import main
from flask import g, url_for, render_template, redirect, request
from app import db
from app.models import Registrant
from app.decorators import InSession
from app.services import SessionManager
from app.services.nvris_client import NVRISClient
from app.main.forms import FormAB6
from app.services.steps import Step_AB_6

@main.route('/ab/preview', methods=["GET", "POST"])
@InSession
def ab6_preview_sign():
    reg = g.registrant
    form = FormAB6(
        signature_string = reg.try_value('signature_string')
    )
    nvris_client = NVRISClient(reg)

    if request.method == "POST" and form.validate_on_submit():
        step = Step_AB_6(form.data)
        if step.run():
            # add signature img but do not save till we have signed form too.
            reg.update(form.data)

            # sign the form and cache the image for next step
            # TODO one form for each election(s)
            signed_ab_form = nvris_client.get_ab_form()
            if signed_ab_form:
                reg.update({'ab_form':signed_ab_form})
                reg.save(db.session)
                session_manager = SessionManager(reg, step)
                return redirect(session_manager.get_redirect_url())

    # always generate a new unsigned form for preview
    preview_img = nvris_client.get_ab_form()
    return render_template('ab/preview-sign.html', preview_img=preview_img, registrant=reg, form=form)

