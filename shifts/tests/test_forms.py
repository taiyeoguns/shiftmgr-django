from ..forms import AddTaskForm
from ..models import Shift, Manager, Member, Priority, Status
from mixer.backend.django import mixer
import pytest


@pytest.mark.django_db
class TestForms:
    def test_AddTaskForm_is_valid(self):

        manager = mixer.blend(Manager, user__is_manager=True)
        shift = mixer.blend(Shift, manager=manager)
        member = mixer.blend(Member, user__is_member=True)
        shift.members.add(member)
        mixer.blend(Priority)
        mixer.blend(Status)

        form = AddTaskForm(
            data={
                "uuid": shift.uuid,
                "member": member.id,
                "title": "Task 1",
                "start": "07:59 PM",
                "priority": 1,
                "status": 1,
            },
            suuid=shift.uuid,
        )

        assert form.is_valid() is True
