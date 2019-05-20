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
    IDENTITY_CARD_TYPE = Choices(
        (1, 'ID', '身份证'),
        (2, 'PASSPORT', '护照'),
    )

    PLATFORM_TYPE = Choices(
        (1, 'IOS', 'iOS'),
        (2, 'ANDROID', 'Android'),
        (3, 'WEB', 'Web'),
    )

    CHANNEL_TYPE = Choices(
        (1, 'MOBILE', '手机'),
        (2, 'EMAIL', '邮箱'),
    )

    GENDER_TYPE = Choices(
        (1, 'MALE', '男'),
        (2, 'FEMALE', '女'),
    )

    nickname = models.CharField(max_length=30, verbose_name=_('nickname'))
    avatar = models.CharField(max_length=128, blank=True, verbose_name=_('avatar'))
    email = models.EmailField(blank=True, unique=True, verbose_name=_('email'))
    mobile = models.CharField(max_length=30, blank=True, unique=True, verbose_name=_('mobile'))
    gender = models.SmallIntegerField(default=-1, verbose_name=_('gender'))
    date_birth = models.DateField(null=True, blank=True, verbose_name=_('birthday'))
    age = models.SmallIntegerField(default=-1, verbose_name=_('age'))
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name=_('ip'))
    id_number = models.CharField(max_length=128, blank=True, verbose_name=_('id'))
    id_type = models.SmallIntegerField(default=-1, verbose_name=_('id type'))
    country = models.CharField(max_length=128, blank=True, verbose_name='国家')
    province = models.CharField(max_length=128, blank=True, verbose_name='省份')
    city = models.CharField(max_length=128, blank=True, verbose_name='城市')
    is_new = models.BooleanField(default=True, verbose_name='是否为新用户')
    is_staff = models.BooleanField(default=False, verbose_name='是否为员工')
    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        ),
    )
    channel = models.SmallIntegerField(default=CHANNEL_TYPE.EMAIL, verbose_name='注册类型')
    platform = models.SmallIntegerField(default=PLATFORM_TYPE.WEB, verbose_name='注册平台')
    is_active = models.BooleanField(default=True, verbose_name='是否有效')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='用户')
    oauth_type = models.SmallIntegerField(verbose_name='第三方类型')
    oauth_id = models.CharField(max_length=255, verbose_name='第三方id')
    oauth_token = models.CharField(max_length=255, verbose_name='第三方token')
    expires = models.IntegerField(blank=True, verbose_name='过期时间')
    is_active = models.BooleanField(default=True, verbose_name='是否有效')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        app_label = 'user'
        db_table = 'user_oauth'
