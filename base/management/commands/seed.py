from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from shifts.models import Shift, Manager, Member
from mixer.backend.django import mixer


class Command(BaseCommand):
    help = "Seeds the database with initial data"

    def _get_user(self):
        fname = mixer.faker.first_name()
        lname = mixer.faker.last_name()
        username = f"{fname}_{lname}".lower()
        email = f"{fname}.{lname}@shiftmanager.local".lower()

        return {"username": username, "fname": fname, "lname": lname, "email": email}

    def _clear(self):
        self.stdout.write("Clearing data")

        get_user_model().objects.all().delete()
        Manager.objects.all().delete()
        Member.objects.all().delete()
        Shift.objects.all().delete()

    def add_arguments(self, parser):
        parser.add_argument(
            "--num", type=int, default=10, help="Number of items to create"
        )

    def handle(self, *args, **options):

        self._clear()  # clear existing table entries

        self.stdout.write("Starting...")

        self.stdout.write("Seeding Users")

        # set bounds not less than 5 or greater than 100
        if options["num"] < 5:
            options["num"] = 5

        if options["num"] > 100:
            options["num"] = 100

        for i in range(options["num"]):

            # seed users
            _user = self._get_user()

            if i < round(0.4 * options["num"]) - 1:
                user = mixer.blend(
                    get_user_model(),
                    username=_user.get("username"),
                    first_name=_user.get("fname"),
                    last_name=_user.get("lname"),
                    email=_user.get("email"),
                    is_manager=True,
                )

                mixer.blend(Manager, user=user)
            else:
                user = mixer.blend(
                    get_user_model(),
                    username=_user.get("username"),
                    first_name=_user.get("fname"),
                    last_name=_user.get("lname"),
                    email=_user.get("email"),
                    is_member=True,
                )

                mixer.blend(Member, user=user)

        # seed shifts
        self.stdout.write("Seeding Shifts")

        for i in range(options["num"]):
            mixer.blend(
                Shift,
                date=mixer.faker.date_between(start_date="-4w"),
                manager=mixer.SELECT,
            )

        self.stdout.write("Done.")
