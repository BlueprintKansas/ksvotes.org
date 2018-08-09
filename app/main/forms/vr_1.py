from flask_wtf import FlaskForm
from wtforms import BooleanField, RadioField
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext

class FormVR1(FlaskForm):
    is_citizen = RadioField(
        lazy_gettext(u'1VR_citizen'),
        choices=[('no', lazy_gettext(u'choice_no')), ('yes', lazy_gettext(u'choice_yes'))],
        default='no', # always require user action
        validators=[DataRequired(message=lazy_gettext(u'Required'))]
    )
    #is_citizen = BooleanField(lazy_gettext(u'1VR_citizen'), validators=[DataRequired(message=lazy_gettext(u'Required'))])
    is_eighteen = BooleanField(lazy_gettext(u'1VR_18'))
