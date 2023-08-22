from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login_page, name="login"),
    path("signup", views.signup, name="signup"),
    path("settings", views.settings, name="profile"),
    path("saved", views.saved, name="saved"),
    path("logout", views.logout_user, name="logout")
]
