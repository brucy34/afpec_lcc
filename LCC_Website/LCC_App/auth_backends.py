from django.contrib.auth.backends import ModelBackend
from .models import Concurrent
from django.contrib.auth.hashers import check_password


class ConcurrentBackend(ModelBackend):
    def authenticate(self, request, code=None, password=None, **kwargs):
        try:
            concurrent = Concurrent.objects.get(concurrent_code=code)

            # Check if the user is active
            if not concurrent.is_active:
                return None

            if check_password(password, concurrent.password):
                return concurrent
        except Concurrent.DoesNotExist:
            return None

    def get_user(self, user_code):
        try:
            return Concurrent.objects.get(concurrent_code=user_code)
        except Concurrent.DoesNotExist:
            return None
