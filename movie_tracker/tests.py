from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from movie_tracker.models import Movie, Profile

class FilmDiarieZViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(user=self.user, bio='Test Bio', social_media=['Twitter'])
        self.client.login(username='testuser', password='testpassword')

    def test_login_view(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)

    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_diary_view(self):
        response = self.client.get(reverse('diary'))
        self.assertEqual(response.status_code, 200)

    def test_watchlist_view(self):
        response = self.client.get(reverse('watchlist'))
        self.assertEqual(response.status_code, 200)

    def test_add_to_top3_view(self):
        response = self.client.post(reverse('add_to_top3'), {'movie_name': 'Movie1', 'details': 'Details1', 'poster': 'poster1.jpg'})
        self.assertEqual(response.status_code, 302)

    def test_delete_movie_view(self):
        movie = Movie.objects.create(user=self.user, movie_name='TestMovie', is_watchlist=True)
        response = self.client.get(reverse('delete_movie', args=[movie.id]))
        self.assertEqual(response.status_code, 302)

    def test_favorites_view(self):
        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 200)


    def test_add_to_favorites_view(self):
        movie = Movie.objects.create(user=self.user, movie_name='TestMovie', details='MovieDetails', poster='poster.jpg')
        response = self.client.get(reverse('add_to_favorites', args=[movie.id]))
        self.assertEqual(response.status_code, 302)

    def test_profile_view(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_like_review_view(self):
        movie = Movie.objects.create(user=self.user, movie_name='TestMovie', details='MovieDetails', poster='poster.jpg')
        response = self.client.get(reverse('like_review', args=[movie.id]))
        self.assertEqual(response.status_code, 200)

    def test_timeline_view(self):
        response = self.client.get(reverse('timeline', kwargs={'filter_type': 'all'}))
        self.assertEqual(response.status_code, 200)
