from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.

class Country(models.Model):
    country_name = models.CharField(max_length=100, unique=True)
    country_code = models.CharField(max_length=3, unique=True)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.country_name


class City(models.Model):
    users = models.ManyToManyField(User, related_name="cities")
    city_name = models.CharField(max_length=50)
    lat = models.FloatField(verbose_name="latitude")
    lon = models.FloatField(verbose_name="longitude")
    city_country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="cities")
    wiki_page = models.TextField()
    image_url = models.CharField(max_length=1000)

    class Meta:
        verbose_name_plural = "Cities"
        unique_together = ('lat', 'lon')

    def __str__(self):
        return self.city_name
