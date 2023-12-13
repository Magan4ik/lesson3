from django.contrib import admin
from weather import models

@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_display = ('city_name', 'city_country')
    list_filter = ('users', 'city_country')

@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_display = ('country_name',)
