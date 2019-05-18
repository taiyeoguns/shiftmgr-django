import os
import random
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from mixer.backend.django import mixer

from shifts.models import Manager, Member, Priority, Shift, Status, Task


class Command(BaseCommand):
    help = "Seeds the database with initial data"

    def _get_user(self):
        """Generate data for user

        Returns:
            Dictionary -- User details
        """
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
        """Clear database tables before seeding
        """
        self.stdout.write("Clearing data")

        get_user_model().objects.all().delete()
        Manager.objects.all().delete()
        Member.objects.all().delete()
        Shift.objects.all().delete()
        Priority.objects.all().delete()
        Status.objects.all().delete()
        Group.objects.all().delete()

    def _create_super_user(self):
        return get_user_model().objects.create_superuser(
            "admin",
            "admin@shiftmanager.local",
            os.getenv("DEFAULT_ADMIN_PASSWORD"),
            first_name="Admin",
            last_name="User",
        )

    def _set_up_roles(self):
        """Set up groups and permissions for users
        """
        admin, manager, member = (
            Group.objects.get_or_create(name=name)[0]
            for name in ("Admin", "Manager", "Member")
        )

        # get permissions for models
        content_types = ContentType.objects.get_for_models(Manager, Member, Shift, Task)
        permissions = Permission.objects.filter(content_type__in=content_types.values())

        manager_permissions = (
            perm
            for perm in permissions
            if perm.codename
            in ("view_shift", "change_shift", "add_task", "change_task")
        )

        member_permissions = (
            perm
            for perm in permissions
            if perm.codename in ("view_shift", "view_task", "change_task")
        )

        admin.permissions.add(*permissions)
        manager.permissions.add(*manager_permissions)
        member.permissions.add(*member_permissions)

        return {"admin": admin, "manager": manager, "member": member}

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

        # create super user
        self.stdout.write("Creating Superuser")
        self._create_super_user()

        # get roles
        _roles = self._set_up_roles()

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
                    password=make_password(os.getenv("DEFAULT_USER_PASSWORD")),
                    is_manager=True,
                )

                user.groups.add(_roles.get("manager"))

                mixer.blend(Manager, user=user)
            else:
                user = mixer.blend(
                    get_user_model(),
                    username=_user.get("username"),
                    first_name=_user.get("fname"),
                    last_name=_user.get("lname"),
                    email=_user.get("email"),
                    phone=_user.get("phone"),
                    password=make_password(os.getenv("DEFAULT_USER_PASSWORD")),
                    is_member=True,
                )

                user.groups.add(_roles.get("member"))

                mixer.blend(Member, user=user)

        # seed shifts
        self.stdout.write("Seeding Shifts")

        mid = round(0.4 * options["num"])

        for i in range(options["num"]):

            if i <= mid:
                mixer.blend(
                    Shift,
                    date=datetime.today() + timedelta(days=i + 1),
                    manager=mixer.SELECT,
                )
            else:
                mixer.blend(
                    Shift,
                    date=datetime.today() - timedelta(days=i + 1),
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
