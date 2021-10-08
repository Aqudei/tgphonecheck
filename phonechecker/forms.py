from django import forms
from phonechecker.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit


class TelethonLoginForm(forms.Form):
    """TelethonLoginForm definition."""

    # TODO: Define form fields here
    code = forms.CharField()
    batch_id = forms.CharField()


class UploadForm(forms.ModelForm):
    """
    docstring
    """

    def __init__(self, *args, **kwargs):
        super(UploadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Upload CSV containing phone numbers and specify its column number',
                'file',
                'phone_column'
            ),
        )

    class Meta:
        """
        docstring
        """
        model = Upload
        fields = '__all__'
