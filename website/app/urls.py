from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import UserPasswordResetForm

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login_page, name="login"),
    path("signup", views.signup, name="signup"),
    path("settings", views.settings, name="profile"),
    path("saved", views.saved, name="saved"),
    path("logout", views.logout_user, name="logout"),
    path("reset-password", auth_views.PasswordResetView.as_view(template_name="app/password-reset-email.html", form_class=UserPasswordResetForm),
         name="reset_password"),
    path("reset-password-sent", views.redirect_home_1,
         name="password_reset_done"),
    path("reset/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view(template_name="app/password-reset-enter.html"),
         name="password_reset_confirm"),
    path("reset-password-complete", views.redirect_home_2,
         name="password_reset_complete"),
]
