from flask_wtf import FlaskForm
from wtforms import SelectField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Regexp, Optional
from flask_babel import lazy_gettext

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

    def pre_validate(self, form):
        # Prevent "not a valid choice" error
        pass

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = "|".join(valuelist)
        else:
            self.data = ""

# based on
# https://stackoverflow.com/questions/8463209/how-to-make-a-field-conditionally-optional-in-wtforms
class OptionalUnlessFieldContains(Optional):

    def __init__(self, other_field_name, value, *args, **kwargs):
        self.other_field_name = other_field_name
        self.value = value
        super(OptionalUnlessFieldContains, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if self.value not in other_field.data:
            super(OptionalUnlessFieldContains, self).__call__(form, field)


class FormAB1(FlaskForm):
    elections = MultiCheckboxField(lazy_gettext(u'1AB_select_election'),
        choices=[], # defer till runtime
        validators=[DataRequired(message=lazy_gettext(u'Required'))]
        )

    party = SelectField(lazy_gettext(u'1AB_select_party'),
        choices=[('', lazy_gettext(u'1AB_select_party')), ('Democratic', 'Democratic'), ('Republican', 'Republican')],
        validators=[OptionalUnlessFieldContains('elections', 'Primary')]
        )

