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
        u.user_permissions.add
        if u:
            raise ValidationException("account exist")

        nickname = generate("en")
        user = User.objects.create_user(nickname, password, email=account, platform=platform, channel=channel)
        login(request, user, backend='apps.user.backends.UserBackend')

        return Response(data=self.serializer_class(user).data, status=status.HTTP_200_OK)


class VCodeView(APIView):

    permission_classes = (
        permissions.AllowAny,
    )
    parser_classes = (JSONParser,)

    def post(self, request):
        account = request.data.get('account')
        verification_type = int(request.data.get('vtype'))

        code_list = [str(i) for i in range(0, 10)]
        vcode = "".join(random.sample(code_list, 6))
        redis_cli = RedisClient()
        r = redis_cli.connection()

        if verification_type == VCodeType.BindPhone.value:
            user = request.user
            if isinstance(user, AnonymousUser):
                raise ClientException("user not login")

            message = BIND_PHONE_MESSAGE % (vcode,)
            sms_cli = SMSClient()
            sms_cli.send(account, message)
            r.setex(BIND_PHONE_KEY % (account,), vcode, REDIS_DEFAULT_EXPIRE_SECONDS)

        elif verification_type == VCodeType.PasswordEmailReset.value:
            user = User.objects.filter(email=account, is_active=True).first()
            if not user:
                raise ClientException("user not found")

            message = PASSWORD_EMAIL_RESET_MESSAGE % (vcode,)
            email_cli = EmailClient()
            email_cli.send_mail("重置密码", message, settings.DEFAULT_FROM_EMAIL, [account])
            r.setex(PASSWORD_RESET_KEY % (account,), vcode, REDIS_DEFAULT_EXPIRE_SECONDS)

        elif verification_type == VCodeType.PasswordMobileReset.value:
            user = User.objects.filter(mobile=account, is_active=True).first()
            if not user:
                raise ClientException("user not found")

            message = BIND_PHONE_MESSAGE % (vcode,)
            sms_cli = SMSClient()
            sms_cli.send(account, message)
            r.setex(PASSWORD_RESET_KEY % (account,), vcode, REDIS_DEFAULT_EXPIRE_SECONDS)
        else:
            pass

        return Response(status=status.HTTP_200_OK)


class VCodeCheckView(APIView):

    permission_classes = (
        permissions.AllowAny,
    )
    parser_classes = (JSONParser,)

    def post(self, request):
        account = request.data.get('account')
        v_type = request.data.get('v_type')
        v_code = request.data.get('v_code')

        if v_type == VCodeType.PasswordEmailReset.value:
            user = User.objects.filter(email=account, is_active=True).first()
            if not user:
                raise ClientException("user not found")
        elif v_type == VCodeType.PasswordMobileReset.value:
            user = User.objects.filter(mobile=account, is_active=True).first()
            if not user:
                raise ClientException("user not found")
        else:
            raise ClientException("vtype not permitted")

        redis_cli = RedisClient()
        r = redis_cli.connection()
        code_sent = r.get(PASSWORD_RESET_KEY % (user.id,))
        if not code_sent:
            raise ValidationException("account error")

        if code_sent != v_code:
            raise ValidationException("vcode error")

        return Response(status=status.HTTP_200_OK)


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


class UserPhoneView(APIView):

    permission_classes = (
        permissions.IsAuthenticated,
    )
    parser_classes = (JSONParser,)
    serializer_class = UserBaseSerializer

    def post(self, request):
        user = request.user
        vcode = request.data.get('vcode')
        mobile = request.data.get('account')

        redis_cli = RedisClient(decode_responses=True)
        r = redis_cli.connection()
        code_sent = r.get(BIND_PHONE_KEY % (user.id, ))
        if not code_sent:
            raise ValidationException("account error")

        if code_sent != vcode:
            raise ValidationException("vcode error")

        user.mobile = mobile
        user.save()
        return Response(self.serializer_class(user).data, status=status.HTTP_200_OK)


class UserProfileEditView(APIView):

    permission_classes = (
        permissions.IsAuthenticated,
    )
    parser_classes = (JSONParser,)
    serializer_class = UserBaseSerializer

    def post(self, request):
        nickname = request.data.get('nickname')
        avatar = request.data.get('avatar')

        user = request.user
        if nickname and user.nickname != nickname:
            user.nickname = nickname

        if avatar and user.avatar != avatar:
            user.avatar = avatar

        user.save()
        return Response(self.serializer_class(user).data, status=status.HTTP_200_OK)


