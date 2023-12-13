from django.db import models

# Create your models here.

class Human(models.Model):
    proff_choice = (
        ("star", "star"),
        ("director", "director")
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)
    profession = models.CharField(max_length=10, choices=proff_choice)

    class Meta:
        unique_together = ("first_name", "last_name", "profession")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Genre(models.Model):
    genre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.genre

class Movie(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField(verbose_name="Year of Release")
    runtime = models.IntegerField(verbose_name="Run Time in minutes")
    rating = models.FloatField()
    votes = models.IntegerField()
    meta_score = models.FloatField(verbose_name="MetaScore")
    gross = models.FloatField()
    genres = models.ManyToManyField(Genre, related_name="movies")
    certification = models.CharField(max_length=200)
    director = models.ManyToManyField(Human, related_name="films")
    stars = models.ManyToManyField(Human, related_name="movies")
    description = models.TextField()

    def __str__(self):
        return self.name


