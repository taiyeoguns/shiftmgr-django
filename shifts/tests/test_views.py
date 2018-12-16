from django.test import RequestFactory
from mixer.backend.django import mixer
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from shifts.views import index
import pytest


@pytest.fixture(scope='module')
def factory():
    return RequestFactory()


@pytest.fixture
def user():
    return mixer.blend(get_user_model())


@pytest.fixture
def shift():
    return mixer.blend('shifts.Shift')


@pytest.mark.django_db
class TestViews:
    def test_shifts_index_authenticated(self, user, factory):
        path = reverse('shifts:index')
        request = factory.get(path)
        request.user = user
        response = index(request)
        assert response.status_code == 200

    def test_shifts_index_unauthenticated(self, factory):
        path = reverse('shifts:index')
        request = factory.get(path)
        request.user = AnonymousUser()
        response = index(request)
        assert response.status_code == 302
        assert reverse('login') in response.url
