from django import forms


class TelethonLoginForm(forms.Form):
    """TelethonLoginForm definition."""

    # TODO: Define form fields here
    code = forms.CharField()
    batch_id = forms.CharField()


class UploadForm(forms.Form):
    """
    docstring
    """
    file = forms.FileField()
