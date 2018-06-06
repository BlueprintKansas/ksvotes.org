from app.main import main
from flask import g, url_for, render_template, redirect, request
from app.main.forms import FormVR5
from app.models import Registrant
from app.decorators import InSession

@main.route('/vr/identification', methods=["GET", "POST"])
def vr5_identification():
    form = FormVR5()
    if request.method == "POST" and form.validate_on_submit():
        return jsonify({"post": "success"})
    return render_template('vr/identification.html', form=form)
