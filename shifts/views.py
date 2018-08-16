from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return HttpResponse("<h1>Shifts Page<h1>")


def home(request):
    # return HttpResponse("<h2>home page</h2>")
    return render(request, 'site/index.html', {})