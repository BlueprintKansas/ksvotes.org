from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired
from flask_babel import gettext

class FormVR4(FlaskForm):
	party = SelectField(gettext('4_party'),
                            validators=[DataRequired(message=gettext('Required'))],
							 choices=[
								 ('', gettext('4_party')),
								 ('democrat', 'Democrat'),
								 ('republican', 'Republican'),
								 ('unafilliated', 'Unafilliated'),
								 ('libertarian', 'Libertarian'),
							 ]
						)
