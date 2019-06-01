from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser

from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from apps.user.models import User
from apps.user.serializers import UserBaseSerializer
from apps.kauth.models import KRole, KResource
from apps.kauth.serializers import KRoleSerializer, KRoleCreateSerializer, KRoleUpdateSerializer
from core.exceptions import ValidationException


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


class UserKRolesView(generics.GenericAPIView):
    permission_classes = (
        permissions.AllowAny,
    )
    serializer_class = UserBaseSerializer

    def post(self, request, pk=None):
        role_id = request.data.get('k8s_role_id')
        k8s_role = KRole.objects.get(pk=role_id)
        if not k8s_role.is_active:
            raise ValidationException("k8s role error")
        user = User.objects.get(pk=pk)
        user.k8s_roles.add(k8s_role)
        user.save()
        return Response(data=self.serializer_class(user).data, status=status.HTTP_201_CREATED)

    def get(self, request, pk=None):
        user = User.objects.get(pk=pk)
        return Response(data=self.serializer_class(user).data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        role_id = request.data.get('k8s_role_id')
        k8s_role = KRole.objects.get(pk=role_id)
        if not k8s_role.is_active:
            raise ValidationException("k8s role error")

        user = User.objects.get(pk=pk)
        user.k8s_roles.remove(k8s_role)
        user.save()
        user.refresh_from_db()
        return Response(data=self.serializer_class(user).data, status=status.HTTP_200_OK)


class KRoleViewSet(viewsets.GenericViewSet):
    model = KRole
    serializer_class = KRoleSerializer
    ordering_fields = ('-id',)
    permission_classes = (
        permissions.AllowAny,
    )

    def get_queryset(self):
        return self.model.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action == 'create':
            return KRoleCreateSerializer
        elif self.action == 'update':
            return KRoleUpdateSerializer
        else:
            return self.serializer_class

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        if data.get("resource_short_name") is not None:
            resource = KResource.objects.get(short_name=data.get("resource_short_name"))
        elif data.get("resource_name") is not None:
            resource = KResource.objects.get(resource_name=data.get("resource_name"))
        else:
            resource_id = data["resource_id"]
            resource = KResource.objects.get(id=resource_id)

        role = self.model(name=data["name"], namespace=data["namespace"], verbs=data["verbs"])
        role.save()

        role.k8s_resources.add(resource)
        role.save()
        return Response(data=self.serializer_class(role).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        role = self.get_object()
        serializer = self.get_serializer_class()(role)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        queryset = self.model.objects.filter(is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        role = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        verbs = data['verbs']
        role.verbs = verbs
        role.save()
        role.refresh_from_db()
        return Response(data=self.serializer_class(role).data, status=status.HTTP_200_OK)
