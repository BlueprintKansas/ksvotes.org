from flask_wtf import FlaskForm
from wtforms import BooleanField,StringField, SelectField
from wtforms.validators import DataRequired
from flask_babel import gettext
from app.main.helpers import RequiredIfBool

class FormVR2(FlaskForm):
	prefix = SelectField(gettext('2_prefix'),
							 choices=[
								 ('', gettext('2_prefix')),
								 ('mr', 'Mr.'),
								 ('mrs', 'Mrs.'),
								 ('miss', 'Miss'),
								 ('ms', 'Ms.')
							 ]
						)
	name_first = StringField(gettext('2_first'), validators=[DataRequired(message=gettext('Required'))])
	name_middle = StringField(gettext('2_middle'))
	name_last = StringField(gettext('2_last'), validators=[DataRequired(message=gettext('Required'))])
	suffix = SelectField(gettext('2_suffix'),
							 choices=[
								 ('', gettext('2_suffix')),
								 ('jr', 'Jr.'),
								 ('sr', 'Sr.'),
								 ('ii', 'II'),
								 ('iii', 'III'),
								 ('iv', 'IV'),
							 ]
						)
	has_prev_name = BooleanField(gettext('2_has_prev_name'))
	prev_prefix = SelectField(gettext('2a_prev_prefix'),
							 choices=[
								 ('', gettext('2a_prev_prefix')),
								 ('mr', 'Mr.'),
								 ('mrs', 'Mrs.'),
								 ('miss', 'Miss'),
								 ('ms', 'Ms.')
							 ]
						)
	prev_name_first = StringField(gettext('2a_prev_first'), validators=[RequiredIfBool('has_prev_name', message=gettext('Required'))])
	prev_name_middle = StringField(gettext('2a_prev_middle'))
	prev_name_last = StringField(gettext('2a_prev_last'), validators=[RequiredIfBool('has_prev_name', message=gettext('Required'))])
	prev_suffix = SelectField(gettext('2a_prev_suffix'),
							 choices=[
								 ('', gettext('2a_prev_suffix')),
								 ('jr', 'Jr.'),
								 ('sr', 'Sr.'),
								 ('ii', 'II'),
								 ('iii', 'III'),
								 ('iv', 'IV'),
							 ]
						)
