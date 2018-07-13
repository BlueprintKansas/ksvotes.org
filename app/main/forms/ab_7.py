from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext

class FormAB7(FlaskForm):
	affirmation = BooleanField(lazy_gettext(u'AB7_affirm'), validators=[DataRequired(message=lazy_gettext(u'Required'))])
