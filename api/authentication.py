from rest_framework.authentication import TokenAuthe6ntication as BaseAuthToken


class TokenAuthentication(BaseAuthToken):
    keyword = "Bearer"
