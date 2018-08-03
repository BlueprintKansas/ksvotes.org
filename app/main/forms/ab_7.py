from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField
from wtforms.validators import DataRequired, Optional
from flask_babel import lazy_gettext
from app.main.helpers import construct_county_choices

class FormAB7(FlaskForm):
    affirmation = BooleanField(lazy_gettext(u'AB7_affirm'), validators=[DataRequired(message=lazy_gettext(u'Required'))])

    county = SelectField(lazy_gettext(u'0_county'),
        validators=[Optional()],
        choices=construct_county_choices(lazy_gettext(u'0_county'))
    )
