from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from shifts.models import Shift, Manager, Member, Priority, Status
from mixer.backend.django import mixer
import random


class Command(BaseCommand):
    help = "Seeds the database with initial data"

    def _get_user(self):
        suffix = mixer.faker.pyint()
        fname = mixer.faker.first_name()
        lname = mixer.faker.last_name()
        username = f"{fname}{lname}{suffix}".lower()
        email = f"{username}@shiftmanager.local".lower()
        phone = mixer.faker.phone_number()

        return {
            "username": username,
            "fname": fname,
            "lname": lname,
            "email": email,
            "phone": phone,
        }

    def _clear(self):
        self.stdout.write("Clearing data")

        get_user_model().objects.all().delete()
        Manager.objects.all().delete()
        Member.objects.all().delete()
        Shift.objects.all().delete()
        Priority.objects.all().delete()
        Status.objects.all().delete()

    def add_arguments(self, parser):
        parser.add_argument(
            "--num", type=int, default=10, help="Number of items to create"
        )

        parser.add_argument(
            "--clear", action="store_true", help="Clear database before seeding"
        )

    def handle(self, *args, **options):

        if options["clear"]:
            self._clear()  # clear existing table entries

        self.stdout.write("Starting...")

        # set bounds not less than 5 or greater than 50
        if options["num"] < 5:
            options["num"] = 5

        if options["num"] > 50:
            options["num"] = 50

        self.stdout.write("Seeding Priorities")
        mixer.cycle(3).blend(
            Priority, title=(title for title in ("High", "Medium", "Low"))
        )

        self.stdout.write("Seeding Statuses")
        mixer.cycle(2).blend(
            Status, title=(title for title in ("Ongoing", "Completed"))
        )

        self.stdout.write("Seeding Users")

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
                    phone=_user.get("phone"),
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
                    phone=_user.get("phone"),
                    is_member=True,
                )

                mixer.blend(Member, user=user)

        # seed shifts
        self.stdout.write("Seeding Shifts")

        for i in range(options["num"]):
            mixer.blend(
                Shift,
                date=mixer.faker.date_between(start_date="-10y", end_date="+10y"),
                manager=mixer.SELECT,
            )

        # assign shift for each member
        self.stdout.write("Seeding members to shifts")

        members = Member.objects.all()
        shifts = Shift.objects.all()

        for i in range(options["num"]):
            member = random.choice(members)
            shift = random.choice(shifts)

            member.shifts.add(shift)

        self.stdout.write("Done.")
