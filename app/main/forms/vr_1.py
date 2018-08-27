from flask_wtf import FlaskForm
from wtforms import BooleanField, RadioField, widgets
from wtforms.widgets import html_params
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext
from markupsafe import Markup

class InlineListWidget(widgets.ListWidget):
    def __call__(self, field, **kwargs):
        self.html_tag = 'div'
        kwargs.setdefault("id", field.id)
        html = ["<%s %s>" % (self.html_tag, html_params(**kwargs))]
        for subfield in field:
            if self.prefix_label:
                html.append("<div class='form-check form-check-inline'>%s %s</div>" % (subfield.label, subfield()))
            else:
                html.append("<div class='form-check form-check-inline'>%s %s</div>" % (subfield(), subfield.label))
        html.append("</%s>" % self.html_tag)
        return Markup("".join(html))

class RadioBooleanField(RadioField):
    widget = InlineListWidget()
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
        choices=[(True, lazy_gettext(u'choice_yes')), (False, lazy_gettext(u'choice_no'))],
        default='False', # always require user action, string not boolean.
        validators=[DataRequired(message=lazy_gettext(u'Required'))]
    )
    is_eighteen = RadioBooleanField(
        lazy_gettext(u'1VR_18'),
        choices=[(True, lazy_gettext(u'choice_yes')), (False, lazy_gettext(u'choice_no'))],
    )
