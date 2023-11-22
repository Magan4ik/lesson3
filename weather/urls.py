from django.urls import path

from weather import views

app_name = 'weather'


urlpatterns = [
    path('', views.weather_widget_view, name='weather_widget'),
]