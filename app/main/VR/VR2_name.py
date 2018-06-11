from app.main import main
from flask import g, url_for, render_template, redirect, request
from app.main.forms import FormVR2
from app.models import Registrant
from app.decorators import InSession

@main.route('/vr/name', methods=["GET", "POST"])
def vr2_name():
    form = FormVR2()
    if request.method == "POST" and form.validate_on_submit():
        return jsonify({"post": "success"})
    return render_template('vr/name.html', form=form)
