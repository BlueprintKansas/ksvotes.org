from app.main import main
from flask import g, url_for, render_template, redirect
from app.models import Registrant
from app.main.forms import FormAB5
from app.decorators import InSession

@main.route('/ab/address', methods=["GET", "POST"])
def ab3_name():
    form = FormAB5()
    if request.method == "POST" and form.validate_on_submit():
        return jsonify({"post": "success"})
    return render_template('/ab/address.html', form=form)
