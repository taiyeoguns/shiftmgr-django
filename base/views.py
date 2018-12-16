from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import RegisterForm
from shifts.models import Member, Manager


# Create your views here.
def home(request):
    return render(request, 'base/home.html', {})


def register(request):
    # get form submission
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        # save, create user type and login if all is right
        if form.is_valid():
            user = form.save()

            if user.is_member:
                Member.objects.create(user=user)
            elif user.is_manager:
                Manager.objects.create(user=user)

            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            messages.success(request, 'Account created successfully')
            return redirect('shifts:index')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})
