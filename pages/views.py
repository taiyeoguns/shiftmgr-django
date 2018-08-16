from django.shortcuts import render


# Create your views here.
def home(request):
    # return HttpResponse("<h2>home page</h2>")
    return render(request, 'site/index.html', {})