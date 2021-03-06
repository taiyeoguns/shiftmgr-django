from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

from shifts.models import Manager, Member


class RegisterForm(forms.Form):
    TYPES = (("member", "Member"), ("manager", "Manager"))

    username = forms.CharField(max_length=25, required=True)
    first_name = forms.CharField(max_length=25, required=True)
    last_name = forms.CharField(max_length=25, required=True)
    phone = forms.CharField(max_length=25)
    email = forms.EmailField(max_length=75, required=True)
    password1 = forms.CharField(max_length=25, label="Password", required=True)
    password2 = forms.CharField(max_length=25, label="Retype Password", required=True)
    type = forms.ChoiceField(
        choices=TYPES, widget=forms.RadioSelect, label="User Type", required=True
    )

    def clean_username(self):
        username = self.cleaned_data["username"].lower()
        r = get_user_model().objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        r = get_user_model().objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def save(self, commit=False):
        user = get_user_model().objects.create_user(
            self.cleaned_data["username"],
            self.cleaned_data["email"],
            self.cleaned_data["password1"],
        )
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.phone = self.cleaned_data.get("phone")

        user_type = self.cleaned_data.get("type")

        if user_type == "member":
            user.is_member = True
            user.save()

            member_group = Group.objects.get(name__iexact="member")
            user.groups.add(member_group)

            Member.objects.create(user=user)

        elif user_type == "manager":
            user.is_manager = True
            user.save()

            manager_group = Group.objects.get(name__iexact="manager")
            user.groups.add(manager_group)

            Manager.objects.create(user=user)

        return user
