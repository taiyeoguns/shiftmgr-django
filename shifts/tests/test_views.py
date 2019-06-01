import datetime
import uuid

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer

from shifts.models import Manager, Member, Shift
from shifts.views import index


@pytest.fixture(scope="module")
def factory():
    return RequestFactory()


@pytest.fixture
def user():
    return mixer.blend(get_user_model())


@pytest.mark.django_db
class TestViews:
    def test_shifts_index_authenticated(self, user, factory):
        path = reverse("shifts:index")
        request = factory.get(path)
        request.user = user
        response = index(request)
        assert response.status_code == 200

    def test_shifts_index_unauthenticated(self, factory):
        path = reverse("shifts:index")
        request = factory.get(path)
        request.user = AnonymousUser()
        response = index(request)
        assert response.status_code == 302
        assert reverse("login") in response.url

    def test_shifts_create(self, user, client):
        path = reverse("shifts:create")

        shift_date = "06/04/2019"
        managers = mixer.cycle(2).blend(Manager)
        members = mixer.cycle(3).blend(Member)

        mgr = managers[0]
        mbrs = [member.id for member in members if member.id < 3]

        client.force_login(user)

        response = client.post(
            path,
            {"shift_date": shift_date, "manager": mgr.id, "members": mbrs},
            follow=True,
        )

        messages = list(response.context["messages"])

        assert reverse("shifts:index") in str(response.redirect_chain)
        assert len(messages) == 1
        assert "Shift added" in str(messages[0])

    def test_shifts_create_does_not_add_existing_date(self, user, client):
        mixer.blend(Shift, date=datetime.date(2019, 4, 6))

        path = reverse("shifts:create")

        shift_date = "06/04/2019"
        managers = mixer.cycle(2).blend(Manager)
        members = mixer.cycle(3).blend(Member)

        mgr = managers[0]
        mbrs = [member.id for member in members if member.id < 3]

        client.force_login(user)

        response = client.post(
            path,
            {"shift_date": shift_date, "manager": mgr.id, "members": mbrs},
            follow=True,
        )

        messages = list(response.context["messages"])

        assert Shift.objects.count() == 1
        assert "exists" in str(messages[0])

    def test_shifts_create_does_not_add_if_form_invalid(self, user, client):
        path = reverse("shifts:create")

        shift_date = "06/04/2019"
        members = mixer.cycle(3).blend(Member)

        mgr = "foo"
        mbrs = [member.id for member in members if member.id < 3]

        client.force_login(user)

        response = client.post(
            path,
            {"shift_date": shift_date, "manager": mgr, "members": mbrs},
            follow=True,
        )

        messages = list(response.context["messages"])

        assert Shift.objects.count() == 0
        assert "issue" in str(messages[0]).lower()

    def test_shifts_detail(self, user, client):
        user.first_name = "Some"
        user.last_name = "Manager"
        user.save()

        manager = mixer.blend(Manager, user=user)
        shift = mixer.blend(Shift, manager=manager)

        path = reverse("shifts:detail", args=[str(shift.uuid)])

        client.force_login(user)

        response = client.get(path)

        assert "Some Manager" in str(response.content)

    def test_shifts_with_non_existing_shift_id_returns_to_home(self, user, client):
        suuid = uuid.uuid4()

        path = reverse("shifts:detail", args=[str(suuid)])

        client.force_login(user)

        response = client.get(path)

        assert reverse("shifts:index") in str(response.url)
