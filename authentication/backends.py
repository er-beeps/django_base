# backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class SpecialUserAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, special=None, **kwargs):
        User = get_user_model()

        if username and password:
            # Authenticate using username and password for regular users
            user = User.objects.filter(username=username).first()
            if user and user.check_password(password):
                return user

        elif special:
            # Authenticate using a token for special users
            try:
                user = User.objects.get(id=special.id)
                return user
            except User.DoesNotExist:
                return None

        return None
