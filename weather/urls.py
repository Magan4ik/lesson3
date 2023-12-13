from django.urls import path

from weather import views

app_name = 'weather'


urlpatterns = [
    path('', views.weather_widget_view, name='weather_widget'),
    path('cityfollow/', views.city_follow_view, name='city_follow'),
    path('cities/', views.city_list_view, name='city_list'),
    path('detail/<str:city_name>/<str:country_code>', views.weather_detail_view, name='weather_detail'),
    path('search/', views.weather_search_view, name='weather_search'),
]