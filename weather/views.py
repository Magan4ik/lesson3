from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from weather import models

from services.weather.open_weather import WeatherInterface

# Create your views here.
@require_http_methods(["GET"])
def weather_widget_view(request: HttpRequest) -> HttpResponse:
    weather = WeatherInterface("Kyiv", country_code="UA")
    index = 0
    weather_data = weather.get_weather_byindex(index, lang="en")
    forecast_data = weather.get_forecast_byindex(index, cnt=7)

    context = {"weather": weather_data, "forecast": forecast_data}
    return render(request, "weather/weather_widget.html", context)

@login_required
@require_http_methods(["GET"])
def city_follow_view(request: HttpRequest, city_name: str, city_id: int) -> HttpResponse:
    city, created = models.CityFollow.objects.get_or_create(city_name=city_name, city_id=city_id)
    if not created:
        if request.user in city.users.all():
            city.users.remove(request.user)
        else:
            city.users.add(request.user)
    else:
        city.users.add(request.user)
    return redirect("weather:city_list")

@login_required
@require_http_methods(["GET"])
def city_list_view(request: HttpRequest) -> HttpResponse:
    cities = request.user.cities.all()
    weather_data_list = list()
    for city in cities:
        wd = WeatherInterface.get_weather_byid(city_id=city.city_id)
        weather_data_list.append(wd)
    return render(request, "weather/city_list.html", {"weather_list": weather_data_list})

@login_required
@require_http_methods(["GET"])
def weather_detail_view(request: HttpRequest, city_id: int) -> HttpResponse:
    weather_data = WeatherInterface.get_weather_byid(city_id)
    forecast_data = WeatherInterface.get_forecast_byid(city_id, cnt=7)
    context = {"weather": weather_data, "forecast": forecast_data}
    return render(request, "weather/weather_widget.html", context)

@login_required
@require_http_methods(["GET"])
def weather_search_view(request: HttpRequest) -> HttpResponse:
    cities = list()
    city_name = request.GET.get('search', '')
    weather = WeatherInterface(city_name=city_name)
    max_index = len(weather.get_city_list())
    for i in range(max_index):
        cities.append(weather.get_weather_byindex(i))

    return render(request, "weather/search.html", {"cities": cities, "city_name": city_name})
