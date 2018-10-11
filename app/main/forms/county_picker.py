from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import Optional
from flask_babel import lazy_gettext
from app.main.helpers import construct_county_choices

class CountyPicker(FlaskForm):
    county = SelectField(lazy_gettext(u'0_county'),
        validators=[Optional()],
        choices=construct_county_choices(lazy_gettext(u'0_county'))
    )
