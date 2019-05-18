import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Group
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory
from django.urls import reverse

from shifts.models import Member

from ..views import RegisterView, home


@pytest.fixture(scope="module")
def factory():
    return RequestFactory()


@pytest.fixture
def groups(db):
    manager, member = (
        Group.objects.get_or_create(name=name)[0] for name in ("Manager", "Member")
    )

    return {"manager": manager, "member": member}


@pytest.mark.django_db
class TestViews:
    def test_home_page_is_displayed(self, factory):
        path = reverse("home")
        request = factory.get(path)
        request.user = AnonymousUser()
        response = home(request)
        assert response.status_code == 200
        assert "Welcome to Shift Manager" in str(response.content)

    def test_register_page_is_displayed(self, factory):
        path = reverse("register")
        request = factory.get(path)
        request.user = AnonymousUser()
        response = RegisterView.as_view()(request)
        assert response.status_code == 200
        assert "Create new account" in str(response.content)

    def test_user_created_through_register_form(self, factory, groups):
        path = reverse("register")
        request = factory.post(
            path,
            {
                "username": "user1",
                "first_name": "First",
                "last_name": "Last",
                "email": "user1@email.com",
                "phone": "123456",
                "password1": "Password123",
                "password2": "Password123",
                "type": "manager",
            },
        )
        SessionMiddleware().process_request(request)
        MessageMiddleware().process_request(request)
        request.user = AnonymousUser()
        response = RegisterView.as_view()(request)
        user = get_user_model().objects.get(username="user1")
        assert response.status_code == 302
        assert user.email == "user1@email.com"
        assert user.is_manager is True
        assert groups["manager"] in user.groups.all()
        assert reverse("shifts:index") in response.url

    def test_error_is_displayed_on_register_form_if_form_is_invalid(self, factory):
        path = reverse("register")
        request = factory.post(path, {"username": "user1"})
        request.user = AnonymousUser()

        response = RegisterView.as_view()(request)
        assert "This field is required" in str(response.content)

    def test_member_is_created_through_register_form(self, factory, groups):
        path = reverse("register")
        request = factory.post(
            path,
            {
                "username": "user1",
                "first_name": "First",
                "last_name": "Last",
                "email": "user1@email.com",
                "phone": "123456",
                "password1": "Password123",
                "password2": "Password123",
                "type": "member",
            },
        )
        SessionMiddleware().process_request(request)
        MessageMiddleware().process_request(request)
        request.user = AnonymousUser()
        RegisterView.as_view()(request)
        user = get_user_model().objects.get(username="user1")
        member = Member.objects.get(user=user)
        assert user.is_member is True
        assert groups["member"] in user.groups.all()
        assert member.id is not None
        assert member.user.username == "user1"
