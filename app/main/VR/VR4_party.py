from app.main import main
from flask import g, url_for, render_template, redirect, request
from app.main.forms import FormVR4
from app.models import Registrant
from app.decorators import InSession

@main.route('/vr/party', methods=["GET", "POST"])
def vr4_party():
    form = FormVR4()
    if request.method == "POST" and form.validate_on_submit():
        return jsonify({"post": "success"})
    return render_template('vr/party.html', form=form)
