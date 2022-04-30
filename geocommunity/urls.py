from django.urls import path
from . import views

app_name = "geocommunity"
urlpatterns = [
    path("", views.CommunitiesView.as_view(), name="index-view"),
]
