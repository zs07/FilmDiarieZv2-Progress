from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True)
    bio = models.TextField(blank=True)
    social_media = models.JSONField(blank=True, null=True)
    all_time_favorites = models.ManyToManyField('Movie', related_name='all_time_favorites', blank=True)
    recently_viewed_movies = models.ManyToManyField('Movie', related_name='viewed_by_profiles', blank=True)
    top3_movies = models.ManyToManyField('Movie', related_name='top3_movies', blank=True)
    followers = models.ManyToManyField(User, related_name='following_profiles', blank=True)
    following = models.ManyToManyField('self', related_name='followers_profiles', symmetrical=False, blank=True)
    objects = models.Manager()

    def _str_(self):
        return f"Profile for {self.user.username}"



class FavoriteMovieManager(models.Manager):
    pass

class FavoriteMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)

    objects = FavoriteMovieManager()

    def _str_(self):
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
    is_top3 = models.BooleanField(default=False)
    review_likes = models.PositiveIntegerField(default=0)  # New field for tracking likes

    # ManyToManyField to store likes for each review
    likes = models.ManyToManyField(User, related_name='movie_likes', blank=True)

    # ManyToManyField to store comments for each movie
    comments = models.ManyToManyField(User, through='Comment', related_name='movie_comments', blank=True)

    objects = models.Manager()

    def _str_(self):
        return self.movie_name

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def _str_(self):
        return f"{self.user.username} - {self.text}"

class Notification(models.Model):

    NOTIFICATION_TYPES = (
        ('F', 'Follow'),
        ('L', 'Like'),
        ('C', 'Comment'),
    )

    notification_type = models.CharField(max_length=1, choices=NOTIFICATION_TYPES)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, blank=True, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    def _str_(self):
        return f"{self.get_notification_type_display()} from {self.sender.username}"