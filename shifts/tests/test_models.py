from django.contrib.auth.models import User
from ..models import Profile
import pytest


@pytest.mark.django_db
class TestModels:
    def test_profile_is_created_when_user_is_created(self):

    	user = User.objects.create_user(username='testuser', email='testuser@email.com', password='password')

    	assert isinstance(user.profile, Profile)
    	assert user.profile is not None

    def test_profile_is_deleted_when_user_is_deleted(self):
    	user = User.objects.create_user(username='testuser', email='testuser@email.com', password='password')
    	user.delete()

    	with pytest.raises(Profile.DoesNotExist):
	    	#user.refresh_from_db()
	    	Profile.objects.get(user=user)


