from django.shortcuts import get_object_or_404, render
from geopy.geocoders import Nominatim
from django.contrib.gis.geos import Point
from accounts.models import Community, MemberRole
from django.views import View
from django.contrib.auth.models import User
from accounts.forms import CommunityCreationForm
from django.http import JsonResponse, HttpResponse
from django.contrib.gis.measure import D
from django.core.serializers import serialize
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.


class CommunitiesView(LoginRequiredMixin, View):
    def get(self, request):
        form = CommunityCreationForm()
        return render(request, "geocommunity/index.html", {"form": form})


@login_required()
def search_nearby(request, lat, long, distance):

    try:
        latitude = float(lat)
        longtitude = float(long)
    except ValueError:
        return HttpResponse(status=404)
    point = Point(longtitude, latitude)
    print(point.coords)
    print(distance)
    print(Community.objects.filter(location__distance_lte=(point, D(km=distance))))
    search_res = serialize(
        "geojson",
        Community.objects.filter(location__distance_lte=(point, D(km=distance))),
        fields=("pk", "name", "description", "location"),
    )

    return HttpResponse(search_res, content_type="application/json")


def join(request, pk):
    community = get_object_or_404(Community, pk=pk)
    if not MemberRole.objects.filter(community=community, user=request.user).exists():
        MemberRole.objects.create(
            community=community, user=request.user, role=MemberRole.MEMBER
        )

    return HttpResponse("Success")
