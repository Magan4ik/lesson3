import hashlib

from django.db import models
from django.contrib.auth.models import AbstractUser

from accounts.managers import UserManager
from accounts.validators import (
    validate_username,
    validate_name,
    validate_birth_date
)


class User(AbstractUser):
    username = models.CharField(max_length=50,
                                unique=True,
                                validators=[validate_username])
    email = models.EmailField(unique=True,
                              max_length=255)
    first_name = models.CharField(max_length=50,
                                  validators=[validate_name])
    last_name = models.CharField(max_length=50,
                                 validators=[validate_name])

    register_token = models.CharField(max_length=5, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        self.username = self.username.lower()
        super().save(*args, **kwargs)


class Profile(models.Model):
    GENDER_CHOICES = (
        ('m', 'Male'),
        ('f', 'Female'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.URLField(max_length=255, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(validators=[validate_birth_date])
    info = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.user} \'s profile'

    def create_gravatar(self):
        md5_hash = hashlib.md5(self.user.email.encode('utf-8')).hexdigest()
        gravatar_url = f'https://www.gravatar.com/avatar/{md5_hash}?d=identicon&s={200}'
        self.avatar = gravatar_url

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
        if not self.avatar:
            self.create_gravatar()
        super().save(*args, **kwargs)


class Follow(models.Model):
    author = models.ForeignKey(User, related_name='follows', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('author', 'user')

    def __str__(self):
        return f"{self.author} follows {self.user}"