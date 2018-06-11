from flask_wtf import FlaskForm
from wtforms import BooleanField,StringField, SelectField
from wtforms.validators import DataRequired, Regexp, Optional
from flask_babel import gettext
from app.main.helpers import RequiredIfBool


class FormAB3(FlaskForm):
    addr = StringField(gettext('3_addr'), validators=[DataRequired(message=gettext('Required'))])
    unit = StringField(gettext('3_unit'))
    city = StringField(gettext('3_city'), validators=[DataRequired(message=gettext('Required'))])
    state = StringField(gettext('3_state'), validators=[DataRequired(message=gettext('Required'))], default='KANSAS', render_kw={'disabled':''})
    zip = StringField(gettext('3_zip'), validators=[DataRequired(message=gettext('Required')), Regexp('^\d{5}$', message=gettext('3_zip_help'))])

    has_mail_addr = BooleanField(gettext('3_has_mail_addr'))
    mail_addr = StringField(gettext('3b_mail_addr'), validators=[RequiredIfBool('has_mail_addr', message=gettext('Required'))])
    mail_unit = StringField(gettext('3b_mail_unit'))
    mail_city = StringField(gettext('3b_mail_city'), validators=[RequiredIfBool('has_prev_addr', message=gettext('Required'))])
    mail_state = StringField(gettext('3b_mail_state'), validators=[RequiredIfBool('has_prev_addr', message=gettext('Required'))])
    mail_zip = StringField(gettext('3b_mail_zip'), validators=[Optional(), RequiredIfBool('has_prev_addr', message=gettext('Required')), Regexp('^\d{5}$', message=gettext('3_zip_help'))])
