# Django
from django.views.generic.list import ListView
from django.shortcuts import render
# Apps
from .models import Result, Coordinate
# Python
import requests
# 3rd party
from geopy.distance import geodesic


def calculate_index(request):
    """
    Calculate the minimun index for a point and a radius
    """
    radius = str(int(request.POST.get('radius', 0))*1000)
    lat = request.POST.get('lat', 0)
    lon = request.POST.get('lon', 0)
    if lat and lon and radius:
        index, points = get_hospitals(lat, lon, radius)
        if index:
            result = Result(
                radius=radius,
                initial_lat=lat,
                initial_lon=lon,
                index=index,
            )
            result.save()
            if points:
                for point in points:
                    coordinate = Coordinate(
                        lat=point[0],
                        lon=point[1],
                        result=result
                    )
                    coordinate.save()
        response = render(request, 'result.html', {'result': index})
    else:
        msg = 'error :('
        response = render(request, 'error.html', {'msg': msg})
    return response


def get_hospitals(latitude, longitude, radius):

    point_ini = (latitude, longitude)
    location = "{},{}".format(latitude, longitude)
    api_endpoint = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+location+"&radius="+radius+"&type=hospital&key=AIzaSyD2axpiyRvdl1CtD9CNpmIPfsJkHIE6ycc"
    print (api_endpoint)
    response = requests.get(api_endpoint)
    resp = response.json()
    distances = []
    points = []
    for place in resp['results']:
        lat = place['geometry']['location']['lat']
        lng = place['geometry']['location']['lng']
        point = (lat, lng)
        points.append(point)
        distances.append(int(get_distance(point_ini, point)))
    index = 0
    for i in distances:
        partial_index = 0
        for j in distances:
            partial_index += (abs(i-j))
        if (partial_index < index) or (index == 0):
            index = partial_index
    return index, points


def get_distance(point_a, point_b):
    """
    Calculate the distance between 2 geographic points
    eg:
        pointa_a: (41.49008, -71.312796)
        pointa_b: (41.499498, -81.695391)
    """
    return geodesic(point_a, point_b).km


class ResultListView(ListView):
    model = Result
    template_name = 'result_list.html'
    context_object_name = 'result_list'
