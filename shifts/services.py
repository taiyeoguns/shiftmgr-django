from service_objects.services import Service
from .models import Shift, Manager, Member
from django.utils import timezone
from django import forms
from .notifications import ShiftCreatedEmail


class GetShifts(Service):

    db_transaction = False

    def process(self):

        try:
            shifts = self.get_shifts()

            past_shifts = [
                shift for shift in shifts if shift.date < timezone.localdate()
            ]
            upcoming_shifts = [
                shift for shift in shifts if shift.date > timezone.localdate()
            ]
            ongoing_shift = [
                shift for shift in shifts if shift.date == timezone.localdate()
            ][0]
        except IndexError:
            ongoing_shift = False

        return {
            "past_shifts": past_shifts,
            "upcoming_shifts": upcoming_shifts,
            "ongoing_shift": ongoing_shift,
        }

    def get_shifts(self):
        return Shift.objects.all()


class AddShift(Service):
    shift_date = forms.DateField(input_formats=["%d/%m/%Y"], required=True)
    manager = forms.ModelChoiceField(
        queryset=Manager.objects.all(), empty_label="", required=True
    )
    members = forms.ModelMultipleChoiceField(
        queryset=Member.objects.all(), required=True
    )

    def process(self):
        date = self.cleaned_data.get("shift_date")
        manager = self.cleaned_data.get("manager")
        members = self.cleaned_data.get("members")

        shift = Shift(manager=manager, date=date)
        shift.save()

        shift.members.add(*members)

        # send email
        ShiftCreatedEmail(shift).send()

        return shift
