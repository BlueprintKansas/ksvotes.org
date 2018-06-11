from app.main import main
from flask import g, url_for, render_template, redirect, request
from app.main.forms import FormVR3
from app.models import Registrant
from app.decorators import InSession

@main.route('/vr/address', methods=["GET", "POST"])
def vr3_address():
    form = FormVR3()
    if request.method == "POST" and form.validate_on_submit():
        return jsonify({"post": "success"})
    return render_template('vr/address.html', form=form)
