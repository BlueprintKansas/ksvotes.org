from flask_wtf import FlaskForm
from wtforms import BooleanField,StringField, SelectField
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext
from app.main.helpers import RequiredIfBool

class FormVR2(FlaskForm):
    prefix = SelectField(lazy_gettext(u'2_prefix'),
                             choices=[
                                 ('', lazy_gettext(u'2_optional_select')),
                                 ('mr', 'Mr.'),
                                 ('mrs', 'Mrs.'),
                                 ('miss', 'Miss'),
                                 ('ms', 'Ms.')
                             ]
                        )
    name_first = StringField(lazy_gettext(u'2_first'), validators=[DataRequired(message=lazy_gettext(u'Required'))])
    name_middle = StringField(lazy_gettext(u'2_middle'))
    name_last = StringField(lazy_gettext(u'2_last'), validators=[DataRequired(message=lazy_gettext(u'Required'))])
    suffix = SelectField(lazy_gettext(u'2_suffix'),
                             choices=[
                                 ('', lazy_gettext(u'2_optional_select')),
                                 ('jr', 'Jr.'),
                                 ('sr', 'Sr.'),
                                 ('ii', 'II'),
                                 ('iii', 'III'),
                                 ('iv', 'IV'),
                             ]
                        )
    has_prev_name = BooleanField(lazy_gettext(u'2_has_prev_name'))
    prev_prefix = SelectField(lazy_gettext(u'2_prev_prefix'),
                             choices=[
                                 ('', lazy_gettext(u'2_prev_prefix')),
                                 ('mr', 'Mr.'),
                                 ('mrs', 'Mrs.'),
                                 ('miss', 'Miss'),
                                 ('ms', 'Ms.')
                             ]
                        )
    prev_name_first = StringField(lazy_gettext(u'2_prev_first'), validators=[RequiredIfBool('has_prev_name', message=lazy_gettext(u'Required'))])
    prev_name_middle = StringField(lazy_gettext(u'2_prev_middle'))
    prev_name_last = StringField(lazy_gettext(u'2_prev_last'), validators=[RequiredIfBool('has_prev_name', message=lazy_gettext(u'Required'))])
    prev_suffix = SelectField(lazy_gettext(u'2_prev_suffix'),
                             choices=[
                                 ('', lazy_gettext(u'2_prev_suffix')),
                                 ('jr', 'Jr.'),
                                 ('sr', 'Sr.'),
                                 ('ii', 'II'),
                                 ('iii', 'III'),
                                 ('iv', 'IV'),
                             ]
                        )
