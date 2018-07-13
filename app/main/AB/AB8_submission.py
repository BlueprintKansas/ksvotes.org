from app.main import main
from flask import g, url_for, render_template, redirect, request
from app import db
from app.models import Registrant, Clerk
from app.decorators import InSession
from app.services import SessionManager
from app.services.steps import Step_AB_7

@main.route('/ab/submission', methods=["GET"])
@InSession
def ab8_submission():
    reg = g.registrant
    session_manager = SessionManager(reg, Step_AB_7())
    if not session_manager.ab_completed():
        return redirect(session_manager.get_redirect_url())

    clerk = Clerk.find_by_county(reg.county)
    return render_template('ab/submission.html', registrant=reg, clerk=clerk)
