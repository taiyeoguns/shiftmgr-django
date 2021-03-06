from django.urls import path
from . import views

app_name = "shifts"
urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("<uuid:uuid>/", views.detail, name="detail"),
    path("tasks/", views.TaskView.as_view(), name="tasks"),
]
