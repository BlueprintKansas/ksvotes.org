from app.main import main
from flask import g, url_for, render_template, redirect, session as http_session
from app.models import Registrant
from app.decorators import InSession

@main.route('/ab1_election_picker', methods=["GET", "POST"])
@InSession
def ab1_election_picker():
    return render_template('ab/election_picker.html')
