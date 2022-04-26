from unicodedata import name
from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    path("newpost", views.NewPost.as_view(), name="newpost"),
    path("", views.PostListView.as_view(), name="postlist-view"),
    path("updateorder/<int:post_id>", views.UpdateOrder.as_view(), name="updateorder"),
    path("deletepost/<int:post_id>", views.DeletePost.as_view(), name="deletepost"),
    path("asyncpost", views.AsynUpdatePost.as_view(), name="asyncpost"),
    path("schedule", views.ScheduleList.as_view(), name="schedule"),
    path("todo", views.HostList.as_view(), name="todo"),
    path("toshare", views.ShareList.as_view(), name="toshare"),
]
