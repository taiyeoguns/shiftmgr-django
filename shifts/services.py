from datetime import datetime

from django import forms
from django.utils import timezone
from service_objects.services import Service

from .models import Manager, Member, Priority, Shift, Status, Task
from .notifications import ShiftCreatedEmail


class GetShifts(Service):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(GetShifts, self).__init__(*args, **kwargs)

    db_transaction = False
    user = None

    def process(self):

        try:
            shifts = self.get_shifts()

            past_shifts = [
                shift for shift in shifts if shift.date < timezone.localdate()
            ]
            upcoming_shifts = [
                shift for shift in shifts if shift.date > timezone.localdate()
            ]
            ongoing_shift = [
                shift for shift in shifts if shift.date == timezone.localdate()
            ][0]
        except IndexError:
            ongoing_shift = False

        return {
            "past_shifts": past_shifts,
            "upcoming_shifts": upcoming_shifts,
            "ongoing_shift": ongoing_shift,
        }

    def get_shifts(self):
        if self.user.is_manager:
            return self.user.manager.shifts.all()
        elif self.user.is_member:
            return self.user.member.shifts.all()
        else:
            return (
                Shift.objects.select_related("manager")
                .prefetch_related("members")
                .all()
            )


class AddShift(Service):
    shift_date = forms.DateField(input_formats=["%d/%m/%Y"], required=True)
    manager = forms.ModelChoiceField(
        queryset=Manager.objects.select_related("user").all(),
        empty_label="",
        required=True,
    )
    members = forms.ModelMultipleChoiceField(
        queryset=Member.objects.select_related("user").all(), required=True
    )

    def process(self):
        date = self.cleaned_data.get("shift_date")
        manager = self.cleaned_data.get("manager")
        members = self.cleaned_data.get("members")

        shift = Shift(manager=manager, date=date)
        shift.save()

        shift.members.add(*members)

        # send email
        ShiftCreatedEmail(shift).send()

        return shift


class GetShift(Service):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(GetShift, self).__init__(*args, **kwargs)

    uuid = forms.UUIDField()

    db_transaction = False
    user = None

    def process(self):
        uuid = self.cleaned_data.get("uuid")

        try:
            shift = (
                Shift.objects.select_related("manager")
                .prefetch_related("members")
                .get(uuid=uuid)
            )
        except Shift.DoesNotExist:
            return False

        if shift:
            if self.user.is_member:
                shift_tasks = shift.tasks.filter(handler=self.user.member)
            else:
                shift_tasks = shift.tasks.all()

            member_tasks = {
                task.handler: shift.tasks.filter(handler=task.handler).count()
                for task in shift.tasks.all()
            }

            groups_data = [
                {"id": member.id, "content": member.user.get_full_name()}
                for member in shift.members.all()
            ]

            timeline_data = [
                {
                    "id": task.id,
                    "content": task.title,
                    "group": task.handler.id,
                    "start": task.start.isoformat(),
                    "end": task.end.isoformat() if task.end else "",
                }
                for task in shift_tasks
            ]

        return {
            "shift": shift,
            "shift_tasks": shift_tasks,
            "member_tasks": member_tasks,
            "groups_data": groups_data,
            "timeline_data": timeline_data,
        }


class AddTask(Service):
    def __init__(self, *args, **kwargs):
        suuid = kwargs.pop("suuid")
        self._members = Member.objects.filter(shifts__uuid=suuid)
        super(AddTask, self).__init__(*args, **kwargs)
        self.fields["member"].queryset = self._members

    _members = None
    _priorities = Priority.objects.all()
    _statuses = Status.objects.all()

    uuid = forms.UUIDField()
    title = forms.CharField()
    start = forms.TimeField(input_formats=["%I:%M %p"], required=True)
    end = forms.TimeField(input_formats=["%I:%M %p"], required=False)
    member = forms.ModelChoiceField(queryset=_members, required=True)
    priority = forms.ModelChoiceField(queryset=_priorities, required=True)
    status = forms.ModelChoiceField(queryset=_statuses, required=True)

    db_transaction = False

    def process(self):
        uuid = self.cleaned_data.get("uuid")
        title = self.cleaned_data.get("title")
        start = self.cleaned_data.get("start")
        end = self.cleaned_data.get("end")
        member = self.cleaned_data.get("member")
        priority = self.cleaned_data.get("priority")
        status = self.cleaned_data.get("status")

        # get shift
        try:
            shift = Shift.objects.get(uuid=uuid)
        except Shift.DoesNotExist:
            return False

        # create task
        if shift:

            if end:
                task = Task.objects.create(
                    title=title,
                    start=timezone.make_aware(datetime.combine(shift.date, start)),
                    end=timezone.make_aware(datetime.combine(shift.date, end)),
                    shift=shift,
                    handler=member,
                    priority=priority,
                    status=status,
                )
            else:
                task = Task.objects.create(
                    title=title,
                    start=timezone.make_aware(datetime.combine(shift.date, start)),
                    shift=shift,
                    handler=member,
                    priority=priority,
                    status=status,
                )

            return task
