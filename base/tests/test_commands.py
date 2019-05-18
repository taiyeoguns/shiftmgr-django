from io import StringIO
from django.core.management import call_command
from django.contrib.auth import get_user_model
from shifts.models import Shift
import pytest


@pytest.mark.django_db
class TestCommands:
    def test_seed_command(self):
        out = StringIO()
        call_command("seed", stdout=out)

        assert get_user_model().objects.filter(is_staff=False).count() == 10
        assert "Done" in out.getvalue()

    def test_seed_command_with_num_argument(self):
        out = StringIO()
        call_command("seed", stdout=out, num=15)

        assert Shift.objects.count() == 15
        assert "Seeding" in out.getvalue()
        assert "Clearing" not in out.getvalue()

    def test_seed_command_with_clear_argument(self):
        out = StringIO()
        call_command("seed", stdout=out, clear=True)

        assert Shift.objects.count() == 10
        assert "Clearing" in out.getvalue()

    def test_seed_command_with_lower_boundary(self):
        call_command("seed", num=-1)

        assert Shift.objects.count() == 5

    def test_seed_command_with_upper_boundary(self):
        call_command("seed", num=100000)

        assert Shift.objects.count() == 50
