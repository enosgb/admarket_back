from django.urls import path

from .views import (
    ChangePasswordView,
    LoginView,
    LogoutView,
    ResetPasswordConfirmView,
    ResetPasswordRequestView,
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("reset_password/", ResetPasswordRequestView.as_view(), name="reset_password"),
    path(
        "reset_password_confirm/",
        ResetPasswordConfirmView.as_view(),
        name="reset_password_confirm",
    ),
    path(
        "change_password/",
        ChangePasswordView.as_view(),
        name="change_password",
    ),
]
