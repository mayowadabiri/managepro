from rest_framework.authentication import TokenAuthentication as BaseAuthToken
from rest_framework.exceptions import AuthenticationFailed

from django.utils.timezone import now
from datetime import timedelta


class TokenAuthentication(BaseAuthToken):
    keyword = "Bearer"

    def authenticate_credentials(self, key):
        user_token = super().authenticate_credentials(key)
        token = user_token[1]
        print(now() - timedelta(days=24))
        if token.created < now() - timedelta(days=7):
            token.delete()
            raise AuthenticationFailed("Token has expired")
        return user_token
