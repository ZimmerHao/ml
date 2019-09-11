from .models import Pod
from .serializers import PodSerializer
from rest_framework import generics
from django.shortcuts import redirect, render, HttpResponse, HttpResponseRedirect
from django.views.generic import RedirectView


class PodListCreate(generics.ListCreateAPIView):
    queryset = Pod.objects.all()
    serializer_class = PodSerializer

class ZeppelinView(RedirectView):
    template_name = "web/login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            print("user authed !")
            redirect("http://console.deepvega.com/hi/zeppelin/tony")
            # return super().get_redirect_url(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            print("user authed !")
            # return super().get_redirect_url(*args, **kwargs)
            redirect("http://console.deepvega.com/hi/zeppelin/tony")
        return render(request, self.template_name)

class ZeppelinView3(RedirectView):
    template_name = "web/login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse('')
        else:
            print("Z3 not authed")

class ZeppelinView4(RedirectView):
    template_name = "web/login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(redirect_to="http://console.deepvega.com/app/zeppelin/tony")
            # return HttpResponseRedirect(redirect_to="http://console.dp.com:3000/?orgId=1")
        else:
            print("Z4 not authed")
            return render(request, self.template_name)

class ZeppelinView5(RedirectView):
    def get(self, request, *args, **kwargs):
        pass
