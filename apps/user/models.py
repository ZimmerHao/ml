import copy

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, Permission, Group
from django.db import models
from model_utils import Choices
from django.utils.translation import gettext_lazy as _

from apps.kauth.models import KPermissionsMixin


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, **kwargs):
        user = self.model(**kwargs)
        user.set_password(kwargs.get('password'))
        user.save(using=self._db)
        return user

    def create_user(self, nickname, password, email=None, mobile=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        if not nickname:
            raise ValueError('The given nickname must be set')
        if not password:
            raise ValueError('The given password must be set')
        if not (email or mobile):
            raise ValueError('The given email or mobile must be set')

        user_params = dict()
        if email:
            email = self.normalize_email(email)
            user_params.update(email=email)
        if mobile:
            user_params.update(mobile=mobile)
        user_params.update(nickname=nickname, password=password)
        user_params.update(**extra_fields)
        user_params = self._format_user_params(**user_params)
        return self._create_user(**user_params)

    def _format_user_params(self, **kwargs):
        user_fields = User._meta.get_fields()
        params = copy.deepcopy(kwargs)
        for field in user_fields:
            field_type = field.get_internal_type()
            field_name = field.name
            if field_type in ('CharField', 'TextField'):
                params[field_name] = str(kwargs[field_name]) if kwargs.get(field_name) else ''
        return params

    def create_superuser(self, nickname, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user_params = dict()
        email = self.normalize_email(email)
        user_params.update(email=email, nickname=nickname, password=password)
        user_params.update(extra_fields)
        return self._create_user(**user_params)

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})


class User(AbstractBaseUser, KPermissionsMixin):
    CHANNEL_TYPE = Choices(
        (1, 'MOBILE', '手机'),
        (2, 'EMAIL', '邮箱'),
    )

    GENDER_TYPE = Choices(
        (1, 'MALE', '男'),
        (2, 'FEMALE', '女'),
    )

    nickname = models.CharField(max_length=255, verbose_name=_('nickname'))
    avatar = models.CharField(max_length=255, blank=True, verbose_name=_('avatar'))
    email = models.EmailField(blank=True, unique=True, verbose_name=_('email'))
    mobile = models.CharField(max_length=30, blank=True, unique=True, verbose_name=_('mobile'))
    gender = models.SmallIntegerField(default=-1, verbose_name=_('gender'))
    birthday = models.DateField(null=True, blank=True, verbose_name=_('birthday'))
    age = models.SmallIntegerField(default=-1, verbose_name=_('age'))
    country = models.CharField(max_length=255, blank=True, verbose_name=_('id type'))
    province = models.CharField(max_length=255, blank=True, verbose_name=_('id type'))
    city = models.CharField(max_length=255, blank=True, verbose_name=_('id type'))
    is_staff = models.BooleanField(default=False, verbose_name=_('id type'))
    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        ),
    )
    channel = models.SmallIntegerField(default=CHANNEL_TYPE.EMAIL, verbose_name=_('id type'))
    is_active = models.BooleanField(default=True, verbose_name=_('id type'))
    date_added = models.DateTimeField(auto_now_add=True, verbose_name=_('id type'))
    date_updated = models.DateTimeField(auto_now=True, verbose_name=_('id type'))

    objects = UserManager()

    USERNAME_FIELD = 'nickname'

    class Meta:
        app_label = 'user'
        db_table = 'user'

    def get_full_name(self):
        # The user is identified by their email address
        return self.nickname

    def get_short_name(self):
        # The user is identified by their email address
        return self.nickname

    def __str__(self):  # __unicode__ on Python 2
        return self.nickname


class UserOAuth(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name=_('id type'))
    oauth_type = models.SmallIntegerField(verbose_name=_('id type'))
    oauth_id = models.CharField(max_length=255, verbose_name=_('id type'))
    oauth_token = models.CharField(max_length=255, verbose_name=_('id type'))
    expires = models.IntegerField(blank=True, verbose_name=_('id type'))
    is_active = models.BooleanField(default=True, verbose_name=_('id type'))
    date_added = models.DateTimeField(auto_now_add=True, verbose_name=_('id type'))
    date_updated = models.DateTimeField(auto_now=True, verbose_name=_('id type'))

    class Meta:
        app_label = 'user'
        db_table = 'user_oauth'
