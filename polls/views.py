import datetime
from django.views.generic.edit import UpdateView
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
from .forms import CreateQuestionForm, UpdateQuestionStatusForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "polls/index.html"

    def get_recent_live_questions(self, request):
        recent_live_questions = Question.objects.filter(
            pub_date__lte=timezone.now(),
            closed=False,
            community__in=request.user.community_set.all(),
        ).order_by("-pub_date")
        if recent_live_questions.count() >= 5:
            recent_live_questions = recent_live_questions[:5]
        return recent_live_questions

    def get_recent_closed_questions(self, request):
        recent_closed_questions = Question.objects.filter(
            pub_date__lte=timezone.now(),
            closed=True,
            community__in=request.user.community_set.all(),
        ).order_by("-pub_date")
        if recent_closed_questions.count() >= 5:
            recent_closed_questions = recent_closed_questions[:5]
        return recent_closed_questions

    def get(self, request):
        recent_live_questions = self.get_recent_live_questions(request)
        recent_closed_questions = self.get_recent_closed_questions(request)
        form = CreateQuestionForm(user=request.user)
        context = {
            "recent_live_questions": recent_live_questions,
            "recent_closed_questions": recent_closed_questions,
            "form": form,
        }

        return render(request, "polls/index.html", context=context)


class QuestionListView(LoginRequiredMixin, ListView):
    context_object_name = "question_list"
    paginate_by = 5
    template_name = "polls/question_list.html"

    def get_queryset(self):
        return Question.objects.filter(
            closed=False, community__in=self.request.user.community_set.all()
        ).order_by("-pub_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.form = CreateQuestionForm(user=self.request.user)
        context["form"] = self.form
        return context


class ResultListView(LoginRequiredMixin, ListView):
    paginate_by = 5
    context_object_name = "question_list"
    template_name = "polls/result_list.html"

    def get_queryset(self):
        self.form = CreateQuestionForm(user=self.request.user)
        return Question.objects.filter(
            closed=True, community__in=self.request.user.community_set.all()
        ).order_by("-pub_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["form"] = self.form
        return context


class QuestionDetailView(LoginRequiredMixin, DetailView):
    model = Question
    template_name = "polls/question_detail.html"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.form = CreateQuestionForm(user=self.request.user)
        context["form"] = self.form
        return context


class QuestionModalView(LoginRequiredMixin, DetailView):
    model = Question
    template_name = "polls/question_detail_modal.html"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultDetailView(LoginRequiredMixin, View):
    def get(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        result_plot = result_graph(question)
        context = {"result_plot": result_plot, "question": question}
        return render(request, "polls/result_detail.html", context=context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.form = CreateQuestionForm(user=self.request.user)
        context["form"] = self.form
        return context


class ResultModalView(LoginRequiredMixin, View):
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


@login_required()
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

        if question.is_voter(request.user):
            try:
                existing_vote = Vote.objects.get(question=question, user=request.user)
                existing_vote.delete()
                error_message = "You changed your vote"

            except Vote.DoesNotExist:
                error_message = None

            Vote.objects.create(
                user=request.user, question=question, choice=selected_choice
            )

            result_plot = result_graph(question)
            return render(
                request,
                "polls/live_result_modal.html",
                {
                    "question": question,
                    "result_plot": result_plot,
                    "error_message": error_message,
                },
            )
        else:
            return render(
                request,
                "polls/question_detail_modal.html",
                {"question": question, "error_message": "You are not a voter"},
            )


class CreateQuestion(LoginRequiredMixin, View):
    def get(self, request):
        form = CreateQuestionForm(user=request.user)
        return render(request, "polls/create_question_form.html", {"form": form})

    def post(self, request):
        form = CreateQuestionForm(request.user, request.POST)
        community_id = int(request.POST.get("community", ""))
        form.instance.author = request.user
        if form.is_valid():

            if not request.user.community_set.filter(id=community_id).exists():
                return render(
                    request,
                    "polls/create_question_form.html",
                    {"form": form, "permissionerror": "You are not in the community"},
                )
            new_question = form.save()

            for i in range(1, len(request.POST)):
                choice_text = request.POST.get(f"choice{i}", "")
                if choice_text != "":
                    try:
                        Choice.objects.create(
                            question=new_question, choice_text=choice_text
                        )
                    except:
                        pass

            return render(request, "polls/success.html", {"question": new_question})
        else:
            return render(request, "polls/create_question_form.html", {"form": form})


def add_choice(request, id):
    return render(request, "polls/choice.html", {"id": id + 1})


class UpdateQuestionStatus(LoginRequiredMixin, View):
    def get(self, request):
        form = UpdateQuestionStatusForm(request.user)
        return render(request, "polls/update_question_status_form.html", {"form": form})

    def post(self, request):
        form = UpdateQuestionStatusForm(request.user, request.POST)
        message = None
        if form.is_valid():
            question = form.cleaned_data["question"]
            closed = form.cleaned_data["closed"]
            question.closed = closed
            question.save()
            form = UpdateQuestionStatusForm(request.user)
            message = "Done.More?"

        return render(
            request,
            "polls/update_question_status_form.html",
            {"form": form, "message": message},
        )
