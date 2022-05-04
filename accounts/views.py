from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.urls import reverse, reverse_lazy
from django.views import View
from wasmtime import Instance
from .forms import CommunityCreationForm, UserProfileForm
from .models import Community, MemberRole, UserProfile
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
            address = {}
            for temp in ["country", "city", "housestreet"]:
                address[temp] = form.cleaned_data[temp]
            if (
                form.cleaned_data["postalcode"]
                and form.cleaned_data["postalcode"] != ""
            ):
                address["postalcode"] = form.cleaned_data["postalcode"]

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

                return render(request, "posts/success.html")
            else:
                error_message = "Location is not in the database, please check again<br>You can try to remove detail so that only country, city, street are left"
        return render(
            request,
            "registration/new_community_form.html",
            {"form": form, "error_message": error_message},
        )

    def get(self, request):

        form = CommunityCreationForm()
        return render(request, "registration/new_community_form.html", {"form": form})


class UserProfileView(View):
    def get(self, request):
        if UserProfile.objects.filter(user=request.user).exists():
            form = UserProfileForm(instance=request.user.userprofile)
            profile = request.user.userprofile

        else:
            form = UserProfileForm()
            profile = None

        return render(
            request, "registration/userprofile.html", {"form": form, "profile": profile}
        )

    def post(self, request):
        try:
            profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            profile = UserProfile(user=request.user)

        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save()
            return render(
                request,
                "registration/profileform.html",
                {
                    "form": UserProfileForm(instance=profile),
                    "success": "Your changes have been saved",
                    "profile": profile,
                },
            )
        else:
            return render(
                request,
                "registration/profileform.html",
                {"form": form, "profile": profile},
            )
