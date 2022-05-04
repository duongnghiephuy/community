from django.urls import path

from . import views

app_name = "polls"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index-view"),
    path("question-list", views.QuestionListView.as_view(), name="question-list-view"),
    path("result-list", views.ResultListView.as_view(), name="result-list-view"),
    path(
        "<int:pk>/",
        views.QuestionDetailView.as_view(),
        name="question-detail-view",
    ),
    path("<int:question_id>/votemodal/", views.votemodal, name="votemodal"),
    path(
        "<int:question_id>/result/",
        views.ResultDetailView.as_view(),
        name="result-detail-view",
    ),
    path(
        "<int:pk>/question",
        views.QuestionModalView.as_view(),
        name="question-detail-modal",
    ),
    path(
        "<int:pk>/questionresult",
        views.ResultModalView.as_view(),
        name="result-detail-modal",
    ),
    path("createquestion", views.CreateQuestion.as_view(), name="createquestion"),
]
