from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from config.containers import FacadeContainer
from services.citites.exceptions import CityOrCountryNotFound

import logging

logger = logging.getLogger("weather")

# Create your views here.
@require_http_methods(["GET"])
def weather_widget_view(request: HttpRequest) -> HttpResponse:
    """Temporary placeholder for main page of weather"""
    city_facade = FacadeContainer.city_info_facade()
    city_info_dto = city_facade.get_full_info_by_name("Kyiv")
    context = {"city_info": city_info_dto}
    return render(request, "weather/weather_widget.html", context)

@login_required
@require_http_methods(["GET"])
def city_follow_view(request: HttpRequest) -> HttpResponse:
    city_name = request.GET.get("city_name")
    country_code = request.GET.get("country_code")
    city_facade = FacadeContainer.city_info_facade()
    
    city_facade.get_or_create_country(city_name=city_name, country_code=country_code)

    city_info_dto = city_facade.get_full_info_by_name(city_name=city_name, country_code=country_code)
    city_facade.subscribe_city(user_id=request.user.pk, city_name=city_info_dto.name)

    return redirect("weather:city_list")

@login_required
@require_http_methods(["GET"])
def city_list_view(request: HttpRequest) -> HttpResponse:
    city_facade = FacadeContainer.city_info_facade()
    weather_data_dict = city_facade.get_user_cities_dict(user_id=request.user.pk)

    return render(request, "weather/city_list.html", {"weather_dict": weather_data_dict})

@login_required
@require_http_methods(["GET"])
def weather_detail_view(request: HttpRequest, city_name: str, country_code: str) -> HttpResponse:

    city_facade = FacadeContainer.city_info_facade()
    city_info_dto = city_facade.get_full_info_by_name(city_name=city_name, country_code=country_code)

    context = {"city_info": city_info_dto}
    return render(request, "weather/weather_widget.html", context)

@login_required
@require_http_methods(["GET"])
def weather_search_view(request: HttpRequest) -> HttpResponse:
    city_name = request.GET.get('search', '')
    city_facade = FacadeContainer.city_info_facade()
    try:
        cities, not_found_cities = city_facade.get_city_or_city_lsit_by_title(title=city_name)
    except CityOrCountryNotFound:
        messages.warning(request, "This country or city was not found")
        cities = list()
        not_found_cities = list()

    context = {"cities": cities,
               "not_found_cities": not_found_cities,
               "city_name": city_name}

    return render(request, "weather/search.html", context)
