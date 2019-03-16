from service_objects.services import Service
from .models import Shift


class GetShifts(Service):
    def process(self):
        shifts = Shift.objects.all()

        return {"past_shifts": shifts, "upcoming_shifts": shifts}
