from django.test import RequestFactory
from mixer.backend.django import mixer
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from ..views import register
import pytest
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware


@pytest.fixture(scope='module')
def factory():
    return RequestFactory()


@pytest.mark.django_db
class TestViews:
    def test_user_created_through_register_form(self, factory):
        path = reverse('register')
        request = factory.post(
            path, {
                'username': 'user1',
                'first_name': 'First',
                'last_name': 'Last',
                'email': 'user1@email.com',
                'phone': '123456',
                'password1': 'Password123',
                'password2': 'Password123'
            })
        SessionMiddleware().process_request(request)
        MessageMiddleware().process_request(request)
        request.user = AnonymousUser
        response = register(request)
        user = get_user_model().objects.get(username='user1')
        assert response.status_code == 302
        assert user.email == 'user1@email.com'
        assert reverse('shifts-index') in response.url
