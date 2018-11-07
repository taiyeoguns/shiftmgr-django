from ..forms import RegisterForm
import pytest


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
                'password2': 'Password123'
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
                'password2': 'Password321'
            })

        assert form.is_valid() is False
        assert 'Enter a valid email address' in str(form.errors)
