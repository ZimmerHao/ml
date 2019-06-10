from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1>Test Home Page</h1>")