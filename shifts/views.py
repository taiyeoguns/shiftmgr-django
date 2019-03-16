from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .services import GetShifts


# Create your views here.
@login_required
def index(request):
    shifts = GetShifts.execute({})
    return render(
        request,
        "shifts/index.html",
        {
            "page_title": "Shifts",
            "past_shifts": shifts.get("past_shifts"),
            "upcoming_shifts": shifts.get("upcoming_shifts"),
        },
    )
