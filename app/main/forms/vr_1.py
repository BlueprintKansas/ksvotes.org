from flask_wtf import FlaskForm
from wtforms import BooleanField, RadioField, widgets
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext

class RadioBooleanField(RadioField):
    widget = widgets.ListWidget()
    option_widget = widgets.RadioInput()

    def process_formdata(self, valuelist):
        if 'False' in valuelist:
            self.data = False
        elif 'True' in valuelist:
            self.data = True
        else:
            self.data = False


class FormVR1(FlaskForm):
    is_citizen = RadioBooleanField(
        lazy_gettext(u'1VR_citizen'),
        choices=[(False, lazy_gettext(u'choice_no')), (True, lazy_gettext(u'choice_yes'))],
        default=False, # always require user action TODO broken
        validators=[DataRequired(message=lazy_gettext(u'Required'))]
    )
    is_eighteen = BooleanField(lazy_gettext(u'1VR_18'))
