from pyexpat import model
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView
from .forms import CommunityCreationForm
from .models import Community, MemberRole

# Create your views here.


class Signup(View):
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("index-view"))
        else:

            return render(
                request,
                "registration/signup.html",
                {"form": form},
            )

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse_lazy("index-view"))
        form = UserCreationForm()
        return render(request, "registration/signup.html", {"form": form})


class CommunityCreate(View):
    def post(self, request):
        form = CommunityCreationForm(request.POST)
        if form.is_valid():
            community = form.save()
            MemberRole.objects.create(
                user=request.user, community=community, role=MemberRole.ADMIN
            )

            return render("posts/success.html")
        else:
            return render(
                request,
                "registration/new_community_form.html",
                {"form": form},
            )

    def get(self, request):

        form = CommunityCreationForm()
        return render(request, "registration/new_community_form.html", {"form": form})


class CommunityView(ListView):
    paginate_by = 5
    model = Community
    template_name = "registration/community.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CommunityCreationForm()
        context["form"] = form
        return context
