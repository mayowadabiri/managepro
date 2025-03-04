from django.urls import path

from .views import RegisterUserView, TokenVerificationView, LoginView

urlpatterns = [
    path("register", RegisterUserView.as_view(), name="register"),
    path("verify", TokenVerificationView.as_view(), name="verify-user"),
    path("login", LoginView.as_view(), name="login-user"),

]
