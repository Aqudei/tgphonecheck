from django import forms
from phonechecker.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit


class TelethonLoginForm(forms.ModelForm):
    """TelethonLoginForm definition."""

    def __init__(self, *args, **kwargs):
        super(TelethonLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(
            Submit('submit', 'Submit', css_class='btn-primary'))

    class Meta:
        exclude = ('done', 'two_factor', 'timestamp')
        model = BotLogin


class UploadForm(forms.ModelForm):
    """
    docstring
    """

    def __init__(self, *args, **kwargs):
        super(UploadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Upload CSV containing phone numbers and specify its column name',
                'file',
                'phone_column'
            ),
        )

        self.helper.add_input(
            Submit('submit', 'Submit', css_class='btn-primary'))

    class Meta:
        """
        docstring
        """
        model = Upload
        fields = '__all__'
