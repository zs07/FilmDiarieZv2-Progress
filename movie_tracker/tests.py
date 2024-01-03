from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from movie_tracker.models import Movie, Profile

class FilmDiarieZViewsTestCase(TestCase):
    def setUp(self):
        # Set up the client, user, and profile for testing
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(user=self.user, bio='Test Bio', social_media=['Twitter'])
        self.client.login(username='testuser', password='testpassword')

    def test_login_view(self):
        # Test the login view
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after successful login

    def test_logout_view(self):
        # Test the logout view
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after logout

    def test_diary_view(self):
        # Test the diary view
        response = self.client.get(reverse('diary'))
        self.assertEqual(response.status_code, 200)  # Expecting a successful response

    def test_watchlist_view(self):
        # Test the watchlist view
        response = self.client.get(reverse('watchlist'))
        self.assertEqual(response.status_code, 200)  # Expecting a successful response

    def test_add_to_top3_view(self):
        # Test the add to top3 view
        response = self.client.post(reverse('add_to_top3'), {'movie_name': 'Movie1', 'details': 'Details1', 'poster': 'poster1.jpg'})
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after adding to top3

    def test_delete_movie_view(self):
        # Test the delete movie view
        movie = Movie.objects.create(user=self.user, movie_name='TestMovie', is_watchlist=True)
        response = self.client.get(reverse('delete_movie', args=[movie.id]))
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after deleting movie

    def test_favorites_view(self):
        # Test the favorites view
        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 200)  # Expecting a successful response

    def test_add_to_favorites_view(self):
        # Test the add to favorites view
        movie = Movie.objects.create(user=self.user, movie_name='TestMovie', details='MovieDetails', poster='poster.jpg')
        response = self.client.get(reverse('add_to_favorites', args=[movie.id]))
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after adding to favorites

    def test_profile_view(self):
        # Test the profile view
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)  # Expecting a successful response

    def test_like_review_view(self):
        # Test the like review view
        movie = Movie.objects.create(user=self.user, movie_name='TestMovie', details='MovieDetails', poster='poster.jpg')
        response = self.client.get(reverse('like_review', args=[movie.id]))
        self.assertEqual(response.status_code, 200)  # Expecting a successful response

    def test_timeline_view(self):
        # Test the timeline view
        response = self.client.get(reverse('timeline', kwargs={'filter_type': 'all'}))
        self.assertEqual(response.status_code, 200)  # Expecting a successful response
