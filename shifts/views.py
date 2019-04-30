import logging
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from .services import GetShifts, AddShift
from .models import Manager, Member
from .forms import AddShiftForm

logger = logging.getLogger(__name__)


@login_required
def index(request):
    """
    Show list of shifts
    """
    shifts = GetShifts.execute({})
    return render(
        request,
        "shifts/index.html",
        {
            "page_title": "Shifts",
            "past_shifts": shifts.get("past_shifts"),
            "upcoming_shifts": shifts.get("upcoming_shifts"),
            "ongoing_shift": shifts.get("ongoing_shift"),
            "managers": Manager.objects.all(),
            "members": Member.objects.all(),
        },
    )


@login_required
def create(request):
    """
    Create new shift
    """
    form = AddShiftForm(request.POST)
    try:
        if form.is_valid():
            shift = AddShift.execute(request.POST)

            messages.success(request, "Shift added successfully")
            logger.info(f"Shift added successfully. id: {shift.id}")
        else:
            messages.error(request, "Issue with items entered. Check and try again.")
    except IntegrityError:
        messages.error(request, "Date already exists")
        logger.error("Date already exists", exc_info=True)
    finally:
        return redirect("shifts:index")


@login_required
def detail(request, uuid):
    """
    Display details of shift
    """
    return render(request, "shifts/detail.html", {"page_title": "Shift Details"})
