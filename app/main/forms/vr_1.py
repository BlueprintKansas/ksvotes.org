from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms.validators import DataRequired
from flask_babel import gettext

class FormVR1(FlaskForm):
    is_citizen = BooleanField(gettext('1_citizen'), validators=[DataRequired(message=gettext('Required'))])
    is_eighteen = BooleanField(gettext('1_18'))
