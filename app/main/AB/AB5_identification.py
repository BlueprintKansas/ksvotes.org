from app.main import main
from flask import g, url_for, render_template, redirect, request
from app.main.forms import FormAB5
from app import db
from app.decorators import InSession
from app.services import SessionManager
from app.services.steps import Step_AB_5

@main.route('/ab/identification', methods=["GET", "POST"])
@InSession
def ab5_identification():
    # skip if permanent AB application
    if g.registrant.ab_permanent:
        return redirect(url_for('main.ab6_preview_sign'))

    ab_id = g.registrant.try_value('ab_identification')
    form = FormAB5(
        ab_identification = ab_id
    )
    clerk = g.registrant.try_clerk()

    if request.method == "POST" and form.validate_on_submit():
        step = Step_AB_5(form.data)
        if step.run():
            g.registrant.update(form.data)
            db.session.commit()
            session_manager = SessionManager(g.registrant, step)
            return redirect(session_manager.get_redirect_url())

    return render_template('ab/identification.html', form=form, clerk=clerk)
