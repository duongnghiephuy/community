from django.shortcuts import render
from geopy.geocoders import Nominatim
from django.contrib.gis.geos import Point
from accounts.models import Community, MemberRole
from django.views import View
from django.contrib.auth.models import User
from accounts.forms import CommunityCreationForm
from django.http import JsonResponse, HttpResponse
from django.contrib.gis.measure import D
from django.core.serializers import serialize

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


def search_nearby(request, address, lat, long, distance):
    if address != "":
        location = geocode_address(address)
        if not location:
            return HttpResponse(status=404)
        latitude = location.latitude
        longtitude = location.longtitude
    else:
        try:
            latitude = float(lat)
            longtitude = float(long)
        except ValueError:
            return HttpResponse(status=404)
    point = Point(longtitude, latitude)
    response = serialize(
        "geojson",
        Community.objects.filter(location__distance_lte=(point, D(km=distance))),
        fields=("name", "description", "location"),
    )
    return JsonResponse(response)
