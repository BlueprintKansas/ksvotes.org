from app.main import main
from flask import g, url_for, render_template, redirect
from app.models import Registrant
from app.decorators import InSession


@main.route('/change-or-apply', methods=["GET", "POST"])
@InSession
def ab1_change_apply():

    return render_template('/change-or-apply.html', form=form)
