from django import template
from django.contrib.auth import get_user_model

from weather.models import CityFollow

User = get_user_model()

register = template.Library()

@register.filter
def follow_city(user: User, city_id: int) -> bool:
    return user.cities.filter(city_id=city_id).exists()