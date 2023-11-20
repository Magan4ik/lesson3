from django.core.mail import send_mail
from django.http import HttpRequest
from django.urls import reverse
from django.utils.crypto import get_random_string

from config.settings import EMAIL_HOST_USER


def send_activation_email(user):
    user.register_token = get_random_string(length=16)
    user.save()
    message = f"""
                Hi, {user.first_name} {user.last_name},
                In order to complete registration on our website, enter the token below in the appropriate field on the website
                Email confirmation token:
                {user.register_token}
                Сopy this token and paste it on the site"""
    send_mail(
        "DJANGO",
        message,
        EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )