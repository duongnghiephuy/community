from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import CustomLoginForm

from . import views

app_name = "accounts"

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            authentication_form=CustomLoginForm, redirect_authenticated_user=True
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    path("signup/", views.Signup.as_view(), name="signup"),
    path("newcommunity", views.CommunityCreate.as_view(), name="newcommunity"),
    path("communityview", views.CommunityView.as_view(), name="community-view"),
]
