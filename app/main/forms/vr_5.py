from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext

class FormVR5(FlaskForm):
	identification = StringField(lazy_gettext('5VR_id'), validators=[DataRequired(message=lazy_gettext('Required'))])
