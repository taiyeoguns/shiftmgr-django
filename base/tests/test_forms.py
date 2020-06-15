from ..forms import RegisterForm
from django.contrib.auth import get_user_model
import pytest


@pytest.fixture
def user():
    return get_user_model().objects.create_user(
        username='testuser', email='testuser@email.com', password='password')


@pytest.mark.django_db
class TestForms:
    def test_RegisterForm_is_valid(self):
        form = RegisterForm(
            data={
                'username': 'user1',
                'first_name': 'First',
                'last_name': 'Last',
                'email': 'user1@email.com',
                'phone': '123456',
                'password1': 'Password123',
                'password2': 'Password123',
                'type': 'member'
            })

        assert form.is_valid() is True

    def test_RegisterForm_is_not_valid(self):
        form = RegisterForm(
            data={
                'username': 'user1',
                'first_name': 'First',
                'last_name': 'Last',
                'email': 'user1@email',
                'phone': '123456',
                'password1': 'Password123',
                'password2': 'Password321',
                'type': 'member'
            })

        assert form.is_valid() is False
        assert 'Enter a valid email address' in str(form.errors)

    def test_RegisterForm_raises_validation_errors(self, user):
        form = RegisterForm(
            data={
                'username': 'testuser',
                'first_name': 'First',
                'last_name': 'Last',
                'email': 'testuser@email.com',
                'phone': '123456',
                'password1': 'Password123',
                'password2': 'Password321'
            })
        assert form.is_valid() is False
        assert 'Username already exists' in str(form.errors)
        assert 'Email already exists' in str(form.errors)
