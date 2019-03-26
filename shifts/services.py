from service_objects.services import Service
from .models import Shift
from django.utils import timezone


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
