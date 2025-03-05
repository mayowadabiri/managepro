from django.urls import path

from .views import RegisterUserView, CodeVerificationView, LoginView, ForgotPasswordView, ResetPasswordView

urlpatterns = [
    path("register", RegisterUserView.as_view(), name="register"),
    path("verify", CodeVerificationView.as_view(), name="verify-code"),
    path("login", LoginView.as_view(), name="login-user"),
    path("forgot_password", ForgotPasswordView.as_view(), name="forgot_password"),
    path("reset_password", ResetPasswordView.as_view(), name="reset_password"),

]
