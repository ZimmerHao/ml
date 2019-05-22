from django.db import models
from model_utils import Choices
from django.utils.translation import gettext_lazy as _


class KResource(models.Model):
    resource_name = models.CharField(max_length=255, verbose_name=_('resource name'))
    short_name = models.CharField(max_length=255, verbose_name=_('resource short name'))
    api_group = models.CharField(max_length=255, verbose_name=_('api group'))
    namespaced = models.BooleanField(default=False, verbose_name=_('is namespace resource'))
    kind = models.CharField(max_length=255, verbose_name=_("resource kind"))
    is_active = models.BooleanField(default=True, verbose_name=_('active status'))
    date_added = models.DateTimeField(auto_now_add=True, verbose_name=_('created date'))
    date_updated = models.DateTimeField(auto_now=True, verbose_name=_('updated date'))

    class Meta:
        app_label = 'kauth'
        db_table = 'k8s_resource'


class KPermission(models.Model):
    VERB_TYPE = Choices(
        "get",
        "list",
        "create",
        "update",
        "patch",
        "watch",
        "proxy",
        "redirect",
        "delete",
        "deletecollection"
        "*"
    )

    resource = models.ForeignKey(
        KResource,
        on_delete=models.CASCADE,
        null=True,
        verbose_name=_("k8s resource"))
    verb = models.CharField(choices=VERB_TYPE, max_length=255, verbose_name=_("k8s verb"))
    is_active = models.BooleanField(default=True, verbose_name=_('active status'))
    date_added = models.DateTimeField(auto_now_add=True, verbose_name=_('created date'))
    date_updated = models.DateTimeField(auto_now=True, verbose_name=_('updated date'))

    class Meta:
        app_label = 'kauth'
        db_table = 'k8s_permission'


class KRole(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("k8s role name"))
    k8s_permissions = models.ManyToManyField(
        KPermission,
        verbose_name=_('k8s permissions'),
        blank=True,
    )
    is_active = models.BooleanField(default=True, verbose_name=_('active status'))
    date_added = models.DateTimeField(auto_now_add=True, verbose_name=_('created date'))
    date_updated = models.DateTimeField(auto_now=True, verbose_name=_('updated date'))

    class Meta:
        app_label = 'kauth'
        db_table = 'k8s_role'


class KPermissionsMixin(models.Model):
    k8s_role = models.ForeignKey(
        KRole,
        verbose_name=_('k8s roles'),
        blank=True,
        help_text=_(
            'The roles this user belongs to. A user will get all k8s permissions '
            'granted to each of their roles.'
        ),
    )

    class Meta:
        abstract = True
