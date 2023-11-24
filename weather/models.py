from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class CityFollow(models.Model):
    users = models.ManyToManyField(User, related_name="cities")
    city_id = models.IntegerField(unique=True)
    city_name = models.CharField(max_length=50)

    def __str__(self):
        return self.city_name
