from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext

class FormAB5(FlaskForm):
	identification = StringField(lazy_gettext(u'5AB_id'), validators=[DataRequired(message=lazy_gettext(u'Required'))])
