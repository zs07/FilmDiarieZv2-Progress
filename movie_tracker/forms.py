from django import forms
from movie_tracker.models import Movie, Profile

class MovieForm(forms.ModelForm):
    is_favorite = forms.BooleanField(required=False)

    class Meta:
        model = Movie
        fields = ['movie_name', 'details', 'poster', 'date', 'rating', 'review', 'is_favorite']

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']