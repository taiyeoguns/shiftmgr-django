import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import View
from service_objects.errors import InvalidInputsError

from .forms import AddShiftForm, AddTaskForm
from .models import Manager, Member, Priority, Shift, Status
from .services import AddShift, AddTask, GetShift, GetShifts

logger = logging.getLogger(__name__)


@login_required
def index(request):
    """
    Show list of shifts
    """
    shifts = GetShifts.execute({}, user=request.user)
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

    try:

        shift = GetShift.execute({"uuid": uuid}, user=request.user)

        if not shift:
            messages.error(
                request,
                "Could not find shift for id provided",
                extra_tags="alert-important",
            )
            return redirect("shifts:index")

    except InvalidInputsError as e:

        messages.error(
            request,
            f"Invalid shift id: {e.errors.get('uuid').as_text()}",
            extra_tags="alert-important",
        )
        return redirect("shifts:index")

    return render(
        request,
        "shifts/detail.html",
        {
            "page_title": "Shift Details",
            "shift": shift["shift"],
            "shift_tasks": shift["shift_tasks"],
            "member_tasks": shift["member_tasks"],
            "groups_data": shift["groups_data"],
            "timeline_data": shift["timeline_data"],
            "priorities": Priority.objects.all(),
            "statuses": Status.objects.all(),
        },
    )


@method_decorator(login_required, name="dispatch")
class TaskView(View):
    def post(self, request):
        suuid = request.POST.get("uuid")
        form = AddTaskForm(request.POST, suuid=suuid)
        shift = Shift.objects.get(uuid=suuid)

        if form.is_valid():
            task = AddTask.execute(request.POST, suuid=request.POST.get("uuid"))

            messages.success(request, "Task added successfully")
            logger.info(f"Task added successfully. id: {task.id}")
        else:
            messages.error(
                request,
                f"Issue with items entered. Check and try again.",
                extra_tags="alert-important",
            )

        return redirect(shift)
