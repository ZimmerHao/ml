import copy

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, Permission, Group
from django.db import models
from model_utils import Choices
from django.utils.translation import gettext_lazy as _


class KPermission(models.Model):
    resource = models.CharField(max_length=255, verbose_name='第三方类型')
    verb = models.CharField(max_length=255, verbose_name='第三方id')
    is_active = models.BooleanField(default=True, verbose_name='是否有效')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        app_label = 'kauth'
        db_table = 'k8s_permission'


class KRole(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("resource"))
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('k8s permissions'),
        blank=True,
    )
    is_active = models.BooleanField(default=True, verbose_name='是否有效')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        app_label = 'kauth'
        db_table = 'k8s_role'


class KPermissionsMixin(models.Model):
    """
    Add the fields and methods necessary to support the Group and Permission
    models using the ModelBackend.
    """
    k8s_roles = models.ManyToManyField(
        KRole,
        verbose_name=_('k8s roles'),
        blank=True,
        help_text=_(
            'The roles this user belongs to. A user will get all k8s permissions '
            'granted to each of their roles.'
        ),
        related_name="user_set",
        related_query_name="user",
    )
    user_k8s_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user k8s permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="user_set",
        related_query_name="user",
    )

    class Meta:
        abstract = True
