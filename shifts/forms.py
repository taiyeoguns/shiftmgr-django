from django import forms
from .models import Manager, Member, Priority, Status


class AddShiftForm(forms.Form):

    shift_date = forms.DateField(input_formats=["%d/%m/%Y"], required=True)
    manager = forms.ModelChoiceField(
        queryset=Manager.objects.all(), empty_label="", required=True
    )
    members = forms.ModelMultipleChoiceField(
        queryset=Member.objects.all(), required=True
    )


class AddTaskForm(forms.Form):
    def __init__(self, *args, **kwargs):
        suuid = kwargs.pop("suuid")
        self._members = Member.objects.filter(shifts__uuid=suuid)
        super(AddTaskForm, self).__init__(*args, **kwargs)
        self.fields["member"].queryset = self._members

    _members = None

    uuid = forms.UUIDField()
    title = forms.CharField()
    start = forms.TimeField(input_formats=["%I:%M %p"], required=True)
    end = forms.TimeField(input_formats=["%I:%M %p"], required=False)
    member = forms.ModelChoiceField(queryset=_members, required=True)
    priority = forms.ModelChoiceField(queryset=Priority.objects.all(), required=True)
    status = forms.ModelChoiceField(queryset=Status.objects.all(), required=True)
