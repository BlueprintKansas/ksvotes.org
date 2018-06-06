from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_babel import gettext

class FormAB5(FlaskForm):
	identification = StringField(gettext('5_id'), validators=[DataRequired(message=gettext('Required'))])
