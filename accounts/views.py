from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.urls import reverse, reverse_lazy
from django.views import View
from .forms import CommunityCreationForm
from .models import Community, MemberRole
from django.contrib.gis.geos import Point
from geopy.geocoders import Nominatim

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


def geocode_address(address):
    geolocator = Nominatim(user_agent="grocery_sharing")
    location = geolocator.geocode(address)
    return location


class CommunityCreate(View):
    def post(self, request):

        error_message = None
        form = CommunityCreationForm(request.POST, request.FILES)
        if form.is_valid():
            address = form.cleaned_data["address"]
            location = geocode_address(address)

            if location:
                name = form.cleaned_data["name"]
                description = form.cleaned_data["description"]
                image = form.cleaned_data["image"]
                community_location = Point(location.longitude, location.latitude)
                community = Community.objects.create(
                    name=name,
                    description=description,
                    location=community_location,
                    image=image,
                )
                MemberRole.objects.create(
                    user=request.user, community=community, role=MemberRole.ADMIN
                )

                return render("posts/success.html")
            else:
                error_message = "String location is not in the database"
        return render(
            request,
            "registration/new_community_form.html",
            {"form": form, "error_message": error_message},
        )

    def get(self, request):

        form = CommunityCreationForm()
        return render(request, "registration/new_community_form.html", {"form": form})
