from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Email, Regexp, Optional
from flask_babel import gettext
from dateutil.relativedelta import relativedelta
import datetime
from app.main.helpers import construct_county_choices


class FormStep0(FlaskForm):
    name_first = StringField(gettext('0_first'), validators=[DataRequired(message=gettext('Required'))])
    name_last = StringField(gettext('0_last'), validators=[DataRequired(message=gettext('Required'))])
    dob = StringField(gettext('0_dob'), validators=[DataRequired(message=gettext('Required'))])
    county = SelectField(gettext('0_county'),
                         validators=[DataRequired(message=gettext('Required'))],
                         choices=construct_county_choices(gettext('0_county'))
                         )
    email = StringField(gettext('0_email'), validators=[DataRequired(message=gettext('Required')), Email(message=gettext('0_email_flag'))])
    phone = StringField(gettext('0_phone'), validators=[Optional(), Regexp('^\d{3}\-\d{3}\-\d{4}$', message=gettext('0_phone_help'))])

    def validate_dob(self, field):
        time_now = datetime.datetime.utcnow()
        time_dob = datetime.datetime.strptime(field.data, '%m/%d/%Y')
        diff = relativedelta(time_now, time_dob).years
        print(diff)
        if diff <= 15:
            field.errors.append(gettext('0_dob_help'))
            return False
        return True
