from unittest import mock
from shifts.services import GetShifts
from shifts.models import Shift
import datetime


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
