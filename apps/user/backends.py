from django.contrib.auth.models import AnonymousUser
from django.db.models import Q

from apps.user.models import User, UserOAuth


class UserBackend(object):

    def authenticate(self, request, account=None, password=None):
        try:
            user = User.objects.filter(email=account).filter(is_active=True).get()
        except User.DoesNotExist:
            return AnonymousUser()

        if not user.check_password(password):
            return None

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id, is_active=True)
        except User.DoesNotExist:
            return None


class OAuth2Backend(object):

    def authenticate(self, request, oauth_id=None, oauth_token=None, login_type=None):
        try:
            user = UserOAuth.objects.get(oauth_id=oauth_id, oauth_type=login_type, is_active=True)
        except UserOAuth.DoesNotExist:
            return AnonymousUser()
        if user.oauth_token != oauth_token:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id, is_active=True)
        except User.DoesNotExist:
            return None

