from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser

from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from apps.user.serializers import UserBaseSerializer
from apps.kauth.models import KPermission, KRole
from apps.kauth.serializers import KPermissionSerializer, KRoleSerializer, KPermissionCreateSerializer, \
    KRoleCreateSerializer
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
    model = KPermission
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


class KPermissionViewSet(viewsets.GenericViewSet):
    model = KPermission
    serializer_class = KPermissionSerializer
    ordering_fields = ('-id',)

    def get_queryset(self):
        return self.model.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return KPermissionCreateSerializer
        else:
            return self.serializer_class

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        user_address = self.model.objects.create(**data)
        return Response(data=self.serializer_class(user_address).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        permission = self.get_object()
        serializer = self.get_serializer_class()(permission)
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
        permission = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        permission.resource = data['resource']
        permission.verb = data['verb']
        permission.save()
        permission.refresh_from_db()
        return Response(data=self.serializer_class(permission).data, status=status.HTTP_200_OK)


class KRoleViewSet(viewsets.GenericViewSet):
    model = KRole
    serializer_class = KRoleSerializer
    ordering_fields = ('-id',)

    def get_queryset(self):
        return self.model.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return KRoleCreateSerializer
        else:
            return self.serializer_class

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        k8s_perm_ids = data['k8s_permission_ids']
        perms = KPermission.objects.filter(id__in=k8s_perm_ids, is_active=True)
        name = data['name']
        role = self.model.objects.create(name=name, k8s_permissions=perms)
        return Response(data=self.serializer_class(role).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        permission = self.get_object()
        serializer = self.get_serializer_class()(permission)
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
        k8s_perm_ids = data['k8s_permission_ids']
        perms = KPermission.objects.filter(id__in=k8s_perm_ids, is_active=True)
        name = data['name']
        role.name = name
        role.k8s_permissions = perms
        role.save()
        role.refresh_from_db()
        return Response(data=self.serializer_class(role).data, status=status.HTTP_200_OK)
