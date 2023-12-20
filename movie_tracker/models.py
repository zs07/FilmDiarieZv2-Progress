from django.db import models
from django.contrib.auth.models import User


class FavoriteMovieManager(models.Manager):
    pass


class FavoriteMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey('movie_tracker.Movie', on_delete=models.CASCADE)

    objects = FavoriteMovieManager()

    def __str__(self):
        return f"{self.user.username} - {self.movie.movie_name}"


class Movie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    movie_name = models.CharField(max_length=255)
    details = models.CharField(max_length=200)
    poster = models.CharField(max_length=200)
    date = models.DateField(null=True, blank=True)
    rating = models.IntegerField(default=0, null=True, blank=True)
    review = models.TextField(blank=True)
    is_watchlist = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return self.movie_name
