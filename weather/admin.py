from django.contrib import admin
from weather import models

# Register your models here.
@admin.register(models.CityFollow)
class CityFollowAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_display = ('city_name',)
    list_filter = ('users', 'city_name')
