from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext

class FormVR1(FlaskForm):
    is_citizen = BooleanField(lazy_gettext(u'1VR_citizen'), validators=[DataRequired(message=lazy_gettext(u'Required'))])
    is_eighteen = BooleanField(lazy_gettext(u'1VR_18'))
