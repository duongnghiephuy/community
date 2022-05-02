from django.urls import path
from . import views

app_name = "geocommunity"
urlpatterns = [
    path("", views.CommunitiesView.as_view(), name="index-view"),
    path(
        "searchnearby/<str:lat>/<str:long>/<int:distance>",
        views.search_nearby,
        name="searchnearby",
    ),
]
