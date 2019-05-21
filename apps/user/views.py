# -*- coding: UTF-8 -*-

import re
import io
import random
import base64

import redis
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import login, logout
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser
from django.conf import settings


from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FileUploadParser, MultiPartParser
from rest_framework.views import APIView

from nickname_generator import generate

from apps.user.models import User
from apps.user.serializers import UserBaseSerializer
from core.exceptions import ValidationException, ClientException
from libs.redis.client import RedisClient
from libs.email.mailgun import EmailClient
from apps.user.constants import *


class LoginView(generics.GenericAPIView):

    permission_classes = (
        permissions.AllowAny,
    )
    parser_classes = (JSONParser,)
    serializer_class = UserBaseSerializer

    def post(self, request):
        account = request.data.get('account')
        password = request.data.get('password')

        user = authenticate(request, account=account, password=password)

        if isinstance(user, AnonymousUser):
            raise ValidationException("user not found")

        if not user:
            raise ValidationException("login error")
        login(request, user, backend='apps.user.backends.UserBackend')
        return Response(data=self.serializer_class(user).data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):

    permission_classes = (
        permissions.IsAuthenticated,
    )
    parser_classes = (JSONParser,)
    serializer_class = UserBaseSerializer

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class SignUpView(generics.GenericAPIView):

    permission_classes = (
        permissions.AllowAny,
    )
    parser_classes = (JSONParser,)
    serializer_class = UserBaseSerializer

    def post(self, request):
        account = request.data.get('account')
        password = request.data.get('password')

        platform = User.PLATFORM_TYPE.WEB
        channel = User.CHANNEL_TYPE.EMAIL

        try:
            validate_email(account)
        except ValidationError:
            raise ValidationException("email error")

        u = User.objects.filter(email=account).first()
        if u:
            raise ValidationException("account exist")

        nickname = generate("en")
        user = User.objects.create_user(nickname, password, email=account, platform=platform, channel=channel)
        login(request, user, backend='apps.user.backends.UserBackend')

        return Response(data=self.serializer_class(user).data, status=status.HTTP_200_OK)


class PasswordResetView(APIView):

    permission_classes = (
        permissions.AllowAny,
    )
    parser_classes = (JSONParser,)
    serializer_class = UserBaseSerializer

    def post(self, request):
        account = request.data.get('account')
        new = request.data.get('new')

        user = User.objects.filter(Q(email=account) | Q(mobile=account)).filter(is_active=True).first()
        if not user:
            raise ValidationException("user not found")

        redis_cli = RedisClient()
        r = redis_cli.connection()
        code_sent = r.get(PASSWORD_RESET_KEY % (user.id,))
        if not code_sent:
            raise ValidationException("vcode error")

        user.set_password(new)
        user.save()

        request.session.flush()
        login(request, user, backend='apps.user.backends.UserBackend')
        return Response(self.serializer_class(user).data, status=status.HTTP_200_OK)


