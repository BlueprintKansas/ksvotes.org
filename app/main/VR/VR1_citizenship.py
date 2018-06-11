from app.main import main
from flask import g, url_for, render_template, redirect, request
from app.main.forms import FormVR1
from app.models import Registrant
from app.decorators import InSession


@main.route('/vr/citizenship', methods=["GET", "POST"])
@InSession
def vr1_citizenship():
    form = FormVR1()
    if request.method == "POST" and form.validate_on_submit():
        print(form.data)
        pass

    return render_template('vr/citizenship.html', form=form)
