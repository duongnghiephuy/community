import datetime
from http.client import HTTPResponse
from pyexpat import model
from re import template
from django.shortcuts import render
from django.http import (
    Http404,
    HttpResponse,
    HttpResponseNotFound,
    HttpResponseRedirect,
    HttpRequest,
)
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, ListView, DetailView
from django.views import View
from django.urls import reverse
from django.utils import timezone
from polls.result_graph import result_graph
from .models import Question, Choice, Vote
from .result_graph import result_graph

# Create your views here.
class IndexView(TemplateView):
    template_name = "polls/index.html"

    def get_recent_live_questions(self):
        recent_live_questions = Question.objects.filter(
            pub_date__lte=timezone.now(), closed=False
        ).order_by("-pub_date")
        if recent_live_questions.count() >= 5:
            recent_live_questions = recent_live_questions[:5]
        return recent_live_questions

    def get_recent_closed_questions(self):
        recent_closed_questions = Question.objects.filter(
            pub_date__lte=timezone.now(), closed=True
        ).order_by("-pub_date")
        if recent_closed_questions.count() >= 5:
            recent_closed_questions = recent_closed_questions[:5]
        return recent_closed_questions

    def get(self, request):
        recent_live_questions = self.get_recent_live_questions()
        recent_closed_questions = self.get_recent_closed_questions()
        context = {
            "recent_live_questions": recent_live_questions,
            "recent_closed_questions": recent_closed_questions,
        }
        return render(request, "polls/index.html", context=context)


class QuestionListView(ListView):
    context_object_name = "question_list"
    paginate_by = 5
    queryset = Question.objects.filter(closed=False).order_by("-pub_date")
    template_name = "polls/question_list.html"


class ResultListView(ListView):
    paginate_by = 5
    context_object_name = "question_list"
    queryset = Question.objects.filter(closed=True).order_by("-pub_date")
    template_name = "polls/result_list.html"


class QuestionDetailView(DetailView):
    model = Question
    template_name = "polls/question_detail.html"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class QuestionModalView(DetailView):
    model = Question
    template_name = "polls/question_detail_modal.html"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultDetailView(View):
    def get(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        result_plot = result_graph(question)
        context = {"result_plot": result_plot, "question": question}
        return render(request, "polls/result_detail.html", context=context)


class ResultModalView(View):
    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        result_plot = result_graph(question)
        share_url = request.build_absolute_uri(
            reverse("polls:result-detail-view", args=(question.id,))
        )
        context = {
            "result_plot": result_plot,
            "question": question,
            "share_url": share_url,
        }
        return render(request, "polls/result_detail_modal.html", context=context)


def votemodal(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if question.closed:
        return render(
            request,
            "polls/question_detail_modal.html",
            {"question": question, "error_message": "This question is closed"},
        )
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/question_detail_modal.html",
            {"question": question, "error_message": "You didn't select a choice"},
        )
    else:
        Vote.objects.create(
            user=request.user, question=question, choice=selected_choice
        )
        result_plot = result_graph(question)
        return render(
            request,
            "polls/live_result_modal.html",
            {"question": question, "result_plot": result_plot},
        )
