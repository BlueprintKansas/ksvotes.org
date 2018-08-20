from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Optional, Regexp
from flask_babel import lazy_gettext

class FormAB5(FlaskForm):
    ab_identification = StringField(
        lazy_gettext(u'5AB_id'),
        validators=[Optional(), Regexp('^K\d{2}[\-]?\d{2}[\-]?\d{4}$', message=lazy_gettext(u'5AB_id_pattern'))]
    )
