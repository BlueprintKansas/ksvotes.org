from app.main import main
from flask import g, url_for, render_template, request, redirect, session as http_session
from app.decorators import InSession
from app.main.forms import FormAB1
from app.services.steps import Step_AB_1
from app import db
from app.services import SessionManager

@main.route('/ab/election_picker', methods=["GET", "POST"])
@InSession
def ab1_election_picker():
    form = FormAB1()
    if request.method == "POST" and form.validate_on_submit():
        step = Step_AB_1(form.data)
        if step.run():
            g.registrant.update(form.data)
            g.registrant.last_completed_step = 1
            g.registrant.save(db.session)
            session_manager = SessionManager(g.registrant, step)
            return redirect(session_manager.get_redirect_url())

    return render_template('ab/election_picker.html', form=form)

