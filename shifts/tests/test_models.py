from datetime import date
from unittest import mock

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from mixer.backend.django import mixer

from ..models import Manager, Member, Priority, Shift, Status, Task


@pytest.fixture
def user():
    user = get_user_model().objects.create_user(
        username="testuser", email="testuser@email.com", password="password"
    )
    return user


@pytest.fixture
def shift():
    return mixer.blend("shifts.Shift")


@pytest.mark.django_db
class TestModels:
    def test_manager_can_be_created(self, user):
        user.first_name = "Mgr"
        user.save()

        manager = Manager.objects.create(user=user)

        assert manager.id is not None
        assert manager.user.first_name == "Mgr"
        assert "Mgr" in str(manager)
        assert "Manager" in repr(manager)

    def test_member_can_be_created(self, user):
        user.first_name = "Mbr"
        user.save()

        member = Member.objects.create(user=user)

        assert member.id is not None
        assert isinstance(member.user, get_user_model())
        assert member.user.first_name == "Mbr"
        assert "Mbr" in str(member)
        assert "Member" in repr(member)

    def test_shift_can_be_created(self, user):
        user.first_name = "John"
        user.save()
        manager = Manager.objects.create(user=user)
        shift = Shift.objects.create(manager=manager, date=date(2018, 11, 1))

        assert shift.manager.user.first_name == "John"
        assert shift.id is not None
        assert isinstance(shift.date, date)
        assert str(shift) == "2018-11-01"
        assert "Shift" in repr(shift)

    @mock.patch(
        "shifts.models.timezone.localdate",
        return_value=date(2019, 5, 18),
        autospec=True,
    )
    def test_shift_is_today(self, mock_today):
        shift = mixer.blend(Shift, date=date(2019, 5, 18))

        result = shift.is_today

        mock_today.assert_called_once()

        assert result is True

    def test_task_can_be_created(self, shift):
        task = Task.objects.create(
            shift=shift,
            title="Some Task",
            start=timezone.now(),
            handler=mixer.blend(Member),
            priority=mixer.blend(Priority),
            status=mixer.blend(Status),
        )

        assert task.id is not None
        assert isinstance(task.shift.date, date)
        assert isinstance(task.shift.manager, Manager)
        assert isinstance(task.handler, Member)
        assert str(task) == "Some Task"
        assert "Task" in repr(task)

    def test_priority_representation(self):
        priority = mixer.blend(Priority, title="Priority")

        assert str(priority) == "Priority"
        assert "Priority" in repr(priority)

    def test_status_representation(self):
        status = mixer.blend(Status, title="Status")

        assert str(status) == "Status"
        assert "Status" in repr(status)
