from django import forms
from movie_tracker.models import Movie, Profile
from .models import Comment

# Movie Form with optional 'is_favorite' field
class MovieForm(forms.ModelForm):
    is_favorite = forms.BooleanField(required=False)

    class Meta:
        model = Movie
        fields = ['movie_name', 'details', 'poster', 'date', 'rating', 'review', 'is_favorite']

# Form to update the profile picture
class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']

# Comment Form
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
