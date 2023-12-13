from django.contrib import admin
from movies import models

# Register your models here.
@admin.register(models.Human)
class HumanAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_display = ('last_name', 'first_name', 'profession')
    list_filter = ('profession',)

@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_display = ('genre',)

@admin.register(models.Movie)
class MovieAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ('name', 'year', 'rating', 'runtime')
    list_filter = ('genres', 'stars', 'director', 'year')
    search_fields = ('name', 'description')

