from django.views.generic import TemplateView, View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import redirect, render

from apps.user.models import User
from apps.user.backends import UserBackend


class LoginView(TemplateView):
    template_name = "web/login.html"

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context["page_title"] = "EVERY THING IS HERE"
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('web.index')
        return render(request, self.template_name)

    def post(self, request):
        account = request.POST.get('account')
        password = request.POST.get('password')
        user = authenticate(account=account, password=password)
        if isinstance(user, AnonymousUser):
            return redirect('web.login')
        if not user:
            return redirect('web.login')
        login(request, user, backend='apps.user.backends.UserBackend')
        return redirect('frontend.index')


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('web.login')


class IndexView(TemplateView):

    template_name = 'web/index.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('web.login')
        return render(request, self.template_name)



class FIndex(TemplateView):
    template_name = 'frontend/index.html'
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('web.login')
        return render(request, self.template_name)
