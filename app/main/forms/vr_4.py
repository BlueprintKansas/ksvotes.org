from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext

class FormVR4(FlaskForm):
    party = SelectField(lazy_gettext(u'4_party'),
        validators=[DataRequired(message=lazy_gettext(u'Required'))],
        choices=[
             ('', ''),
             ('democratic', 'Democratic'),
             ('republican', 'Republican'),
             ('unaffiliated', 'Unaffiliated'),
             ('libertarian', 'Libertarian'),
        ]
    )
