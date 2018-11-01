from django.contrib.auth.models import User
from ..models import (Profile, Shift, Manager, Member, Task)
from mixer.backend.django import mixer
from datetime import date
from django.utils import timezone
import pytest


@pytest.fixture
def user():
	user = User.objects.create_user(username='testuser', email='testuser@email.com', password='password')
	return user

@pytest.fixture
def shift():
    return mixer.blend('shifts.Shift')

@pytest.mark.django_db
class TestModels:
    def test_profile_is_created_when_user_is_created(self, user):
    	"""  tests that profile model is created when user is created"""

    	assert isinstance(user.profile, Profile)
    	assert user.profile is not None

    def test_profile_is_deleted_when_user_is_deleted(self, user):
    	""" tests that profile is deleted when user is deleted """
    	user.delete()

    	with pytest.raises(Profile.DoesNotExist):
	    	#user.refresh_from_db()
	    	Profile.objects.get(user=user)

    def test_manager_can_be_created(self, user):
        user.first_name = 'Mgr'
        user.save()

        manager = Manager.objects.create(user=user)

        assert manager.id is not None
        assert manager.user.first_name == 'Mgr'
        assert 'Mgr' in str(manager)

    def test_member_can_be_created(self, user):
        user.first_name = 'Mbr'
        user.save()

        member = Member.objects.create(user=user)

        assert member.id is not None
        assert isinstance(member.user, User)
        assert member.user.first_name == 'Mbr'
        assert 'Mbr' in str(member)


    def test_shift_can_be_created(self, user):
    	user.first_name = 'John'
    	user.save()
    	manager = Manager.objects.create(user=user)
    	shift = Shift.objects.create(manager=manager, date=date(2018, 11, 1))

    	assert shift.manager.user.first_name == 'John'
    	assert shift.id is not None
    	assert isinstance(shift.date, date)

    def test_task_can_be_created(self, shift):
        task = Task.objects.create(shift=shift, title='Some Task', start=timezone.now())

        assert task.id is not None
        assert isinstance(task.shift.date, date)
        assert isinstance(task.shift.manager, Manager)


