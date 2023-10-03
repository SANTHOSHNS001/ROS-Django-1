from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class UsernameOrEmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Try to fetch the user by searching the username field
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            try:
                # Try to fetch the user by searching the email field
                user = UserModel.objects.get(email=username)
            except UserModel.DoesNotExist:
                return None

        if user.check_password(password):
            return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None



