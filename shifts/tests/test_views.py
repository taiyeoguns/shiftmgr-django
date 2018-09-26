from django.test import RequestFactory, TestCase
from mixer.backend.django import mixer
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from shifts.views import index
import pytest


@pytest.mark.django_db
class TestViews(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestViews, cls).setUpClass()
        mixer.blend('shifts.Shift')
        cls.factory = RequestFactory()

    def test_shifts_index_authenticated(self):
        path = reverse('shifts-index')
        request = self.factory.get(path)
        request.user = mixer.blend(User)
        response = index(request)
        assert response.status_code == 200

    def test_shifts_index_unauthenticated(self):
        path = reverse('shifts-index')
        request = self.factory.get(path)
        request.user = AnonymousUser()
        response = index(request)
        assert response.status_code == 302