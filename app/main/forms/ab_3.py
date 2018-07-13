from flask_wtf import FlaskForm
from wtforms import BooleanField,StringField, SelectField
from wtforms.validators import DataRequired, Regexp, Optional
from flask_babel import lazy_gettext
from app.main.helpers import RequiredIfBool


class FormAB3(FlaskForm):
    addr = StringField(lazy_gettext(u'3_addr'), validators=[DataRequired(message=lazy_gettext(u'Required'))])
    unit = StringField(lazy_gettext(u'3_unit'))
    city = StringField(lazy_gettext(u'3_city'), validators=[DataRequired(message=lazy_gettext(u'Required'))])
    state = StringField(lazy_gettext(u'3_state'), validators=[DataRequired(message=lazy_gettext(u'Required'))], default='KANSAS')
    zip = StringField(lazy_gettext(u'3_zip'), validators=[DataRequired(message=lazy_gettext(u'Required')), Regexp('^\d{5}$', message=lazy_gettext(u'3_zip_help'))])

    has_mail_addr = BooleanField(lazy_gettext(u'3_has_mail_addr'))
    mail_addr = StringField(lazy_gettext(u'3_mail_addr'), validators=[RequiredIfBool('has_mail_addr', message=lazy_gettext(u'Required'))])
    mail_unit = StringField(lazy_gettext(u'3_mail_unit'))
    mail_city = StringField(lazy_gettext(u'3_mail_city'), validators=[RequiredIfBool('has_mail_addr', message=lazy_gettext(u'Required'))])
    mail_state = StringField(lazy_gettext(u'3_mail_state'), validators=[RequiredIfBool('has_mail_addr', message=lazy_gettext(u'Required'))])
    mail_zip = StringField(lazy_gettext(u'3_mail_zip'), validators=[Optional(), RequiredIfBool('has_mail_addr', message=lazy_gettext(u'Required')), Regexp('^\d{5}$', message=lazy_gettext(u'3_zip_help'))])
