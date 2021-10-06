from django import forms


class TelethonLoginForm(forms.Form):
    """TelethonLoginForm definition."""

    # TODO: Define form fields here
    code = forms.CharField()
