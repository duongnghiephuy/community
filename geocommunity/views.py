from django.shortcuts import render
from geopy.geocoders import Nominatim
from django.contrib.gis.geos import Point
from accounts.models import Community, MemberRole
from django.views import View
from django.contrib.auth.models import User
from accounts.forms import CommunityCreationForm

# Create your views here.

# String to geo location
def geocode_address(address):
    geolocator = Nominatim(user_agent="grocery_sharing")
    location = geolocator.geocode(address)
    return location


class CommunitiesView(View):
    def get(self, request):
        form = CommunityCreationForm()
        return render(request, "geocommunity/index.html",{"form":form})
