from herald import registry
from herald.base import EmailNotification


@registry.register_decorator()
class ShiftCreatedEmail(EmailNotification):
    template_name = "shift_created"
    subject = "Shift Assigned"

    def __init__(self, shift):
        self.context = {"first_name": shift.manager.user.first_name}
        self.to_emails = [shift.manager.user.email]

    @staticmethod
    def get_demo_args():
        from shifts.models import Shift

        return [Shift.objects.order_by("?")[0]]
