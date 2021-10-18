from django import forms
from phonechecker.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Field, Layout, Fieldset, ButtonHolder, Submit

from phonechecker.tasks import batch


class LoginPhoneNumberForm(forms.Form):
    """TelethonLoginForm definition."""
    phone_number = forms.CharField()
    batch_id = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(LoginPhoneNumberForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('phone_number'),
            Field('batch_id', type="hidden")
        )
        self.helper.add_input(
            Submit('submit-phone', 'Submit Phone Number', css_class='btn-primary'))


class LoginCodeForm(forms.Form):
    """TelethonLoginForm definition."""
    code = forms.CharField()
    batch_id = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(LoginCodeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('code'),
            Field('batch_id', type="hidden")
        )
        self.helper.add_input(
            Submit('submit-code', 'Submit Code', css_class='btn-primary'))


class MySqlForm(forms.ModelForm):
    """
    docstring
    """

    def __init__(self, *args, **kwargs):
        super(MySqlForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Setup MySQL Connection',
                'db_name',
                'db_username',
                'db_password',
                'db_host',
                'db_port',
                'db_table',
                'db_column'
            ),
        )

        self.helper.add_input(
            Submit('submit', 'Submit', css_class='btn-primary'))

    class Meta:
        """
        docstring
        """
        model = MySql
        fields = '__all__'


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
