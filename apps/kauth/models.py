from django.db import models
from django.contrib.postgres.fields import ArrayField
from model_utils import Choices
from django.utils.translation import gettext_lazy as _


class KResource(models.Model):
    resource_name = models.CharField(max_length=255, verbose_name=_('resource name'))
    short_name = models.CharField(max_length=255, blank=True, verbose_name=_('resource short name'))
    api_group = models.CharField(max_length=255, blank=True, verbose_name=_('api group'))
    namespaced = models.BooleanField(default=False, verbose_name=_('is namespace resource'))
    kind = models.CharField(max_length=255, verbose_name=_('resource kind'))
    is_active = models.BooleanField(default=True, verbose_name=_('active status'))
    date_added = models.DateTimeField(auto_now_add=True, verbose_name=_('created date'))
    date_updated = models.DateTimeField(auto_now=True, verbose_name=_('updated date'))

    class Meta:
        app_label = 'kauth'
        db_table = 'k8s_resource'


class KRole(models.Model):

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
        "deletecollection",
        "all"
    )

    name = models.CharField(max_length=255, verbose_name=_("k8s role name"))
    namespace = models.CharField(unique=True, max_length=255, verbose_name=_("k8s namespace name"))
    k8s_resources = models.ManyToManyField(
        KResource,
        verbose_name=_('k8s resources'),
        blank=True,
    )
    verbs = ArrayField(models.CharField(max_length=255), blank=True, verbose_name='k8s api resource verb')
    is_active = models.BooleanField(default=True, verbose_name=_('active status'))
    date_added = models.DateTimeField(auto_now_add=True, verbose_name=_('created date'))
    date_updated = models.DateTimeField(auto_now=True, verbose_name=_('updated date'))

    class Meta:
        app_label = 'kauth'
        db_table = 'k8s_role'


class KRolesMixin(models.Model):

    k8s_roles = models.ManyToManyField(
        KRole,
        verbose_name=_('user k8s roles'),
        blank=True,
        related_name="user_set",
        related_query_name="user",
    )

    class Meta:
        abstract = True
