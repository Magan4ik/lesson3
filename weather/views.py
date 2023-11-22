from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from services.weather.open_weather import WeatherInterface

# Create your views here.
def weather_widget_view(request: HttpRequest) -> HttpResponse:
    weather = WeatherInterface("Kiev", country_code="UA")
    weather_data = weather.get_weather_byindex(0)
    context = {"weather": weather_data}
    return render(request, "weather/weather_widget.html", context)