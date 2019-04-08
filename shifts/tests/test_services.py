from unittest import mock
from shifts.services import GetShifts, AddShift
from shifts.models import Shift, Manager, Member
import datetime
from mixer.backend.django import mixer
import pytest


class TestServices:
    @mock.patch("shifts.services.GetShifts.get_shifts", autospec=True)
    @mock.patch(
        "shifts.services.timezone.localdate",
        return_value=datetime.date(2019, 3, 23),
        autospec=True,
    )
    def test_getshifts(self, mock_date, mock_shifts):
        shift1 = Shift(date=datetime.date(2019, 3, 22))
        shift2 = Shift(date=datetime.date(2019, 3, 23))
        shift3 = Shift(date=datetime.date(2019, 3, 24))

        mock_shifts.return_value = [shift1, shift2, shift3]

        shifts = GetShifts.execute({})

        assert shifts["past_shifts"] is not None
        assert shift1 in shifts["past_shifts"]
        assert shift2 == shifts["ongoing_shift"]
        assert shift3 in shifts["upcoming_shifts"]
        mock_shifts.assert_called_once()

    @mock.patch("shifts.services.Member.objects.all")
    @mock.patch("shifts.services.Manager.objects.all")
    @pytest.mark.django_db
    def test_addshift(self, mock_managers, mock_members):
        shift_date = "06/04/2019"
        managers = mixer.cycle(2).blend(Manager)
        members = mixer.cycle(3).blend(Member)

        mock_managers.return_value = managers
        mock_members.return_value = members

        mgr = managers[0]
        mbrs = [member.id for member in members]

        shift = AddShift.execute(
            {"shift_date": shift_date, "manager": mgr.id, "members": mbrs}
        )

        assert shift.id is not None
        assert shift.manager == mgr
        assert list(shift.members.all()) == members
