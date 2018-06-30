from flask_wtf import FlaskForm
from wtforms import SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Regexp, Optional
from flask_babel import lazy_gettext
from app.main.helpers import list_of_elections

class Select2MultipleField(SelectMultipleField):

    def pre_validate(self, form):
        # Prevent "not a valid choice" error
        pass

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = "|".join(valuelist)
        else:
            self.data = ""

class FormAB1(FlaskForm):
    elections = Select2MultipleField(lazy_gettext('1AB_select_election'),
        choices=list_of_elections(),
        render_kw={"multiple": "multiple"},
        validators=[DataRequired(message=lazy_gettext('Required'))])

