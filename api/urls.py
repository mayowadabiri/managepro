from django.urls import path, include
from api.views import home


urlpatterns = [
    path("home/", home),
    path("auth/", include("user.urls")),
    path("services", include("service.urls")),
    path("subscription", include("subscription.urls")),
]
