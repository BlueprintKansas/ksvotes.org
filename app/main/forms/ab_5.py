from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Optional, Regexp
from flask_babel import lazy_gettext
from app.main.helpers import KS_DL_PATTERN

class KSIDField(StringField):
    def process_formdata(self, valuelist):
        self.data = valuelist[0].replace('-', '').replace('/', '')

class FormAB5(FlaskForm):
    ab_identification = KSIDField(
        lazy_gettext(u'5AB_id'),
        validators=[Optional(), Regexp(KS_DL_PATTERN, message=lazy_gettext(u'5AB_id_pattern'))]
    )
