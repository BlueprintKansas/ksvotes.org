from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.validators import DataRequired, Regexp
from flask_babel import lazy_gettext

class FormVR6(FlaskForm):
	signature_string = HiddenField(lazy_gettext(u'6_sign'), validators=[
		DataRequired(message=lazy_gettext(u'Required')), Regexp('^data:image/png;', message='Bad Format')
	])
