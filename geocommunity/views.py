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


def search_nearby(request, lat, long, distance):

    try:
        latitude = float(lat)
        longtitude = float(long)
    except ValueError:
        return HttpResponse(status=404)
    point = Point(longtitude, latitude)
    search_res = serialize(
        "geojson",
        Community.objects.filter(location__distance_lte=(point, D(km=distance))),
        fields=("pk", "name", "description", "location"),
    )
    print(search_res)
    return HttpResponse(search_res, content_type="application/json")
