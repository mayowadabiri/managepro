from django.urls import path, include


urlpatterns = [
    path("auth/", include("user.urls")),
    path("services/", include("service.urls")),
]
