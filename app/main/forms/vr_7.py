from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext

class FormVR7(FlaskForm):
	affirmation = BooleanField(lazy_gettext('7_affirm'), validators=[DataRequired(message=lazy_gettext('Required'))])
