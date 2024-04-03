from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model


class OAuth2Backend(BaseBackend):
    def authenticate(self, request, public_id=None):

        User = get_user_model()
        try:
            return User.objects.get(public_id=public_id)
        except User.DoesNotExist:
            return

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return
