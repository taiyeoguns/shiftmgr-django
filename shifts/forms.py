from django import forms
from .models import Manager, Member


class AddShiftForm(forms.Form):

    shift_date = forms.DateField(input_formats=["%d/%m/%Y"], required=True)
    manager = forms.ModelChoiceField(
        queryset=Manager.objects.all(), empty_label="", required=True
    )
    members = forms.ModelMultipleChoiceField(
        queryset=Member.objects.all(), required=True
    )
