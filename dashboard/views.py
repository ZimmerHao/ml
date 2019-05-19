# -*- coding: UTF-8 -*-

import redis
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import login, logout
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser, Permission, Group
from django.conf import settings

from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from apps.user.models import User
from apps.user.serializers import UserBaseSerializer
from core.exceptions import ValidationException, ClientException


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


class UserPermissionsView(generics.GenericAPIView):

    model = User
    permission_classes = (
        permissions.AllowAny,
    )
    serializer_class = UserBaseSerializer
    ordering_fields = ('-id',)

    def get_queryset(self):
        return self.model.objects.filter(is_active=True)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        data['user'] = request.user
        user_address = self.model.objects.create(**data)
        return Response(data=self.serializer_class(user_address).data, status=status.HTTP_201_CREATED)

    def list(self, request):
        queryset = self.model.objects.filter(user=request.user, is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserPermissionDetailView(generics.GenericAPIView):

    model = User
    permission_classes = (
        permissions.AllowAny,
    )
    serializer_class = UserBaseSerializer
    ordering_fields = ('-id',)

    def get_queryset(self):
        return self.model.objects.filter(is_active=True)

    def delete(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        data['user'] = request.user
        user_address = self.model.objects.create(**data)
        return Response(data=self.serializer_class(user_address).data, status=status.HTTP_201_CREATED)


class PermissionViewSet(viewsets.GenericViewSet):

    model = Permission
    serializer_class = UserAddressSerializer
    ordering_fields = ('-id',)

    def get_queryset(self):
        return self.model.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return UserAddressCreateSerializer
        else:
            return self.serializer_class

    def create(self, request):

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        data['user'] = request.user
        user_address = self.model.objects.create(**data)
        return Response(data=self.serializer_class(user_address).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        address = self.get_object()
        serializer = self.get_serializer_class()(address)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        queryset = self.model.objects.filter(user=request.user, is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        address = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        address.refresh_from_db()
        return Response(data=self.serializer_class(address).data, status=status.HTTP_200_OK)