from django.shortcuts import render
from geopy.geocoders import Nominatim
from django.contrib.gis.geos import Point
from urllib3 import HTTPResponse
from accounts.models import Community, MemberRole
from django.views import View
from django.contrib.auth.models import User
from accounts.forms import CommunityCreationForm
from django.http import JsonResponse, HttpResponse

# Create your views here.

# String to geo location
def geocode_address(address):
    geolocator = Nominatim(user_agent="grocery_sharing")
    location = geolocator.geocode(address)
    return location


class CommunitiesView(View):
    def get(self, request):
        form = CommunityCreationForm()
        return render(request, "geocommunity/index.html", {"form": form})


def search_nearby(request, address, lat, long):
    if address != "":
        location = geocode_address(address)
        if not location:
            return HTTPResponse(status=404)
        latitude = location.latitude
        longtitude = location.longtitude
    else:
        try:
            latitude = float(lat)
            longtitude = float(long)
        except ValueError:
            return HTTPResponse(status=404)
    return JsonResponse(response)
