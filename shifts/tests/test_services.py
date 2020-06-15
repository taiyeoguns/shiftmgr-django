import uuid
from datetime import date
from unittest import mock

import pytest
from django.utils import timezone
from mixer.backend.django import mixer

from shifts.models import Manager, Member, Priority, Shift, Status, Task
from shifts.services import AddShift, AddTask, GetShift, GetShifts


class TestServices:
    @mock.patch("shifts.services.GetShifts.get_shifts", autospec=True)
    @mock.patch(
        "shifts.services.timezone.localdate",
        return_value=date(2019, 3, 23),
        autospec=True,
    )
    @pytest.mark.django_db
    def test_getshifts(self, mock_date, mock_shifts):
        manager = mixer.blend(Manager)

        shift1 = Shift(date=date(2019, 3, 22), manager=manager)
        shift2 = Shift(date=date(2019, 3, 23), manager=manager)
        shift3 = Shift(date=date(2019, 3, 24), manager=manager)

        mock_shifts.return_value = [shift1, shift2, shift3]

        shifts = GetShifts.execute({}, user=manager.user)

        assert shifts["past_shifts"] is not None
        assert shift1 in shifts["past_shifts"]
        assert shift2 == shifts["ongoing_shift"]
        assert shift3 in shifts["upcoming_shifts"]
        mock_shifts.assert_called_once()

    @mock.patch("shifts.services.Member.objects.all")
    @mock.patch("shifts.services.Manager.objects.all")
    @pytest.mark.django_db
    def test_addshift(self, mock_managers, mock_members, mailoutbox):
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

        m = mailoutbox[0]  # get sent mail

        assert shift.id is not None
        assert shift.manager == mgr
        assert list(shift.members.all()) == members
        assert len(mailoutbox) == 1
        assert m.subject == "Shift Assigned"
        assert mgr.user.first_name in m.body

    @mock.patch(
        "shifts.services.timezone.localdate",
        return_value=date(2019, 5, 28),
        autospec=True,
    )
    @pytest.mark.django_db
    def test_getshifts_returns_manager_shifts(self, mock_date):
        manager1 = mixer.blend(Manager, user__is_manager=True)
        manager2 = mixer.blend(Manager, user__is_manager=True)

        shift1 = mixer.blend(Shift, date=date(2019, 5, 29), manager=manager1)
        shift2 = mixer.blend(Shift, date=date(2019, 5, 30), manager=manager2)

        shifts1 = GetShifts.execute({}, user=manager1.user)

        assert shift1 in shifts1["upcoming_shifts"]
        assert shift2 not in shifts1["upcoming_shifts"]

    @mock.patch(
        "shifts.services.timezone.localdate",
        return_value=date(2019, 5, 28),
        autospec=True,
    )
    @pytest.mark.django_db
    def test_getshifts_returns_member_shifts(self, mock_date):
        member1 = mixer.blend(Member, user__is_member=True)
        member2 = mixer.blend(Member, user__is_member=True)

        shift1 = mixer.blend(Shift, date=date(2019, 5, 29))
        shift2 = mixer.blend(Shift, date=date(2019, 5, 30))

        member1.shifts.add(shift1)
        member2.shifts.add(shift2)

        shifts1 = GetShifts.execute({}, user=member1.user)

        assert shift1 in shifts1["upcoming_shifts"]
        assert shift2 not in shifts1["upcoming_shifts"]

    @pytest.mark.django_db
    def test_getshift_returns_shift(self):
        suuid = uuid.uuid4()

        manager = mixer.blend(Manager, user__is_manager=True)
        ashift = mixer.blend(Shift, uuid=suuid, manager=manager)

        shift = GetShift.execute({"uuid": suuid}, user=manager.user)

        assert shift["shift"] == ashift
        assert shift["shift"].uuid == suuid

    @pytest.mark.django_db
    def test_getshift_does_not_return_shift_with_invalid_id(self):
        suuid = uuid.uuid4()

        manager = mixer.blend(Manager, user__is_manager=True)
        mixer.blend(Shift, manager=manager)

        shift = GetShift.execute({"uuid": suuid}, user=manager.user)

        assert shift is False

    @pytest.mark.django_db
    def test_getshift_returns_shift_tasks_for_member(self):

        member1 = mixer.blend(Member, user__is_member=True)
        manager = mixer.blend(Manager, user__is_manager=True)
        ashift = mixer.blend(Shift, manager=manager)
        task1 = mixer.blend(
            Task,
            shift=ashift,
            handler=member1,
            start=timezone.now(),
            end=timezone.now(),
        )

        member2 = mixer.blend(Member, user__is_member=True)
        task2 = mixer.blend(
            Task,
            shift=ashift,
            handler=member2,
            start=timezone.now(),
            end=timezone.now(),
        )

        shift = GetShift.execute({"uuid": ashift.uuid}, user=member1.user)

        assert task1 in shift["shift_tasks"]
        assert task2 not in shift["shift_tasks"]

    @mock.patch("shifts.services.AddTask.execute")
    @mock.patch("shifts.services.AddTask.is_valid", return_value=True)
    @mock.patch("shifts.services.AddTask._priorities")
    @mock.patch("shifts.services.AddTask._statuses")
    @mock.patch("shifts.services.AddTask._members")
    def test_add_task_unit(
        self, mock_members, mock_statuses, mock_priorities, mock_isvalid, mock_execute
    ):
        with mixer.ctx(commit=False):
            members = mixer.cycle(2).blend(Member, id=(id for id in (1, 2)))
            priorities = mixer.cycle(2).blend(Priority, id=iter((1, 2)))
            statuses = mixer.cycle(2).blend(Status, id=iter((1, 2)))

        mock_members.return_value = members
        mock_statuses.return_value = statuses
        mock_priorities.return_value = priorities

        suuid = uuid.uuid4()
        title = "Task 1"
        start = "09:13"
        end = "10:39"
        member = mock_members()[0].id
        priority = mock_priorities()[0].id
        status = mock_statuses()[0].id

        AddTask.execute(
            {
                "uuid": suuid,
                "member": member,
                "title": title,
                "start": start,
                "end": end,
                "priority": priority,
                "status": status,
            },
            suuid=suuid,
        )

        mock_members.assert_called_once()
        mock_execute.assert_called_with(
            {
                "uuid": suuid,
                "member": member,
                "title": title,
                "start": start,
                "end": end,
                "priority": priority,
                "status": status,
            },
            suuid=suuid,
        )

    @pytest.mark.django_db
    def test_add_task(self):
        manager = mixer.blend(Manager, user__is_manager=True)
        shift = mixer.blend(Shift, manager=manager)
        member = mixer.blend(Member, user__is_member=True)
        shift.members.add(member)
        priorities = mixer.cycle(2).blend(
            Priority, id=iter((1, 2)), title=iter(("High", "Medium"))
        )

        statuses = mixer.cycle(2).blend(
            Status, id=iter((1, 2)), title=iter(("Ongoing", "Completed"))
        )


        title = "Task 1"
        start = "09:13 AM"
        end = "03:39 PM"
        _member = member.id
        priority = priorities[0].id
        status = statuses[0].id

        task = AddTask.execute(
            {
                "uuid": shift.uuid,
                "member": _member,
                "title": title,
                "start": start,
                "end": end,
                "priority": priority,
                "status": status,
            },
            suuid=shift.uuid,
        )

        assert Task.objects.count() == 1
        assert isinstance(task, Task)
        assert task.shift == shift
        assert task in shift.tasks.all()

    @pytest.mark.django_db
    def test_add_task_no_end_date(self):
        manager = mixer.blend(Manager, user__is_manager=True)
        shift = mixer.blend(Shift, manager=manager)
        member = mixer.blend(Member, user__is_member=True)
        shift.members.add(member)
        priorities = mixer.cycle(2).blend(
            Priority, id=iter((1, 2)), title=iter(("High", "Medium"))
        )

        statuses = mixer.cycle(2).blend(
            Status, id=iter((1, 2)), title=iter(("Ongoing", "Completed"))
        )


        title = "Task 1"
        start = "09:13 AM"
        _member = member.id
        priority = priorities[0].id
        status = statuses[0].id

        task = AddTask.execute(
            {
                "uuid": shift.uuid,
                "member": _member,
                "title": title,
                "start": start,
                "priority": priority,
                "status": status,
            },
            suuid=shift.uuid,
        )

        assert Task.objects.count() == 1
        assert isinstance(task, Task)
        assert task.shift == shift
        assert task in shift.tasks.all()

    @pytest.mark.django_db
    def test_add_task_does_not_add_with_wrong_shift_id(self):
        suuid = uuid.uuid4()
        manager = mixer.blend(Manager, user__is_manager=True)
        shift = mixer.blend(Shift, manager=manager)
        member = mixer.blend(Member, user__is_member=True)
        shift.members.add(member)
        priorities = mixer.cycle(2).blend(
            Priority, id=iter((1, 2)), title=iter(("High", "Medium"))
        )

        statuses = mixer.cycle(2).blend(
            Status, id=iter((1, 2)), title=iter(("Ongoing", "Completed"))
        )


        title = "Task 1"
        start = "09:13 AM"
        priority = priorities[0].id
        status = statuses[0].id

        task = AddTask.execute(
            {
                "uuid": suuid,
                "member": member.id,
                "title": title,
                "start": start,
                "priority": priority,
                "status": status,
            },
            suuid=shift.uuid,
        )

        assert Task.objects.count() == 0
        assert task is False
