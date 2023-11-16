from django.views.generic import TemplateView, View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import redirect, render
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from core.exceptions import ValidationException
from nickname_generator import generate
from libs.kubernetes.client import K8SClient

from apps.user.models import User
from apps.user.backends import UserBackend
from rest_framework.authtoken.models import Token


from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED
)
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


@csrf_exempt
@api_view(["GET"])
def auth_api(request):
    data = {'sample_data': 123}
    request_user = str(request.user)
    request_host = str(request.META.get('HTTP_X_FORWARDED_HOST'))
    print(request.META)

    print(request_user)
    print(request_host)

    if request_user not in request_host and request_host != 'console.deepvega.com':
        print(f"You are as user {request_user} but trying to access {request_host}")
        return Response(status=HTTP_401_UNAUTHORIZED)
    else:
        return Response(data, status=HTTP_200_OK)


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

    @permission_classes((AllowAny,))
    def post(self, request):
        account = request.POST.get('account')
        password = request.POST.get('password')
        user = authenticate(account=account, password=password)
        token, _ = Token.objects.get_or_create(user=user)
        if isinstance(user, AnonymousUser):
            return redirect('web.login')
        if not user:
            return redirect('web.login')
        login(request, user, backend='apps.user.backends.UserBackend')
        return redirect('web.index')


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


class SignUpView(TemplateView):
    template_name = "web/login.html"

    def get_context_data(self, **kwargs):
        context = super(SignUpView, self).get_context_data(**kwargs)
        context["page_title"] = "EVERY THING IS HERE"
        return context

    def post(self, request):
        account = request.POST.get('account')
        password = request.POST.get('password')

        try:
            validate_email(account)
        except ValidationError:
            raise ValidationException("email error")

        u = User.objects.filter(email=account).first()
        if u:
            raise ValidationException("account exist")

        nickname = generate("en")
        user = User.objects.create_user(nickname, password, email=account)
        login(request, user, backend='apps.user.backends.UserBackend')
        return redirect('web.index')


class FIndex(TemplateView):
    template_name = 'frontend/index.html'
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('web.login')
        return render(request, self.template_name)


class PodListView(TemplateView):

    template_name = 'web/pod_list.html'

    def get(self, request):
        namespace = request.GET.get("namespace", "default")
        k = K8SClient()
        res = k.get_resources_namespaced(resource="po", namespace=namespace)
        pods = []
        for index, pod in enumerate(res.items):
            pods.append({
                "index": index + 1,
                "pod_name": pod.metadata.name,
                "pod_status": pod.status.phase,
                "pod_namespace": pod.metadata.namespace,
                "created_time": pod.metadata.creation_timestamp,
            })
        return render(request, self.template_name, {"pods": pods})
