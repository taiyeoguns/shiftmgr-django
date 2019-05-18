from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.views.generic import View

from .forms import RegisterForm


# Create your views here.
def home(request):
    return render(request, "base/home.html", {})


class RegisterView(View):
    """ displays and processes registration form """

    template = "registration/register.html"

    def get(self, request):
        form = RegisterForm()
        return render(request, self.template, {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)

        # save, create user type and login if all is right
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get("password1")
            _user = authenticate(username=user.username, password=raw_password)
            login(request, _user)
            messages.success(request, "Account created successfully")
            return redirect("shifts:index")
        else:
            return render(request, self.template, {"form": form})
