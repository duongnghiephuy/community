from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.views import View

# Create your views here.


class Signup(View):
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(reverse("community:index-view"))
        else:

            return render(request, "registration/signup.html", {"form": form})

    def get(self, request):
        form = UserCreationForm()
        return render(request, "registration/signup.html", {"form": form})
