from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import MovieForm, CommentForm
from django.db import IntegrityError
from .models import Movie, FavoriteMovie, Comment
from django.http import JsonResponse

@login_required
def like_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    # Assuming you have a user (ensure the user is logged in before reaching this view)
    user = request.user

    # Check if the user has already liked the movie review
    favorite_movie = FavoriteMovie.objects.filter(user=user, movie=movie).first()

    if favorite_movie:
        # User has already liked, so remove their like
        favorite_movie.delete()
        movie.review_likes -= 1
        liked = False
    else:
        # User has not liked, so add their like
        FavoriteMovie.objects.create(user=user, movie=movie)
        movie.review_likes += 1
        liked = True

    movie.save()

    return JsonResponse({'review_likes': movie.review_likes, 'liked': liked})


def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
        except IntegrityError:
            return render(request, "signup.html", {
                "message": "Email address is already registered."
            })
        login(request, user)
        return redirect("index")

    return render(request, "signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "login.html", {
                "message": "Invalid credentials."
            })

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def index(request):
    return render(request, "base.html")



@login_required
def diary(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user = request.user
            movie.is_watchlist = False

            if form.cleaned_data['is_favorite']:
                movie.is_favorite = True

            movie.save()

            if movie.is_favorite:
                favorite_movie = FavoriteMovie(user=request.user, movie=movie)
                favorite_movie.save()

            return redirect('diary')
    else:
        form = MovieForm()

    movies = Movie.objects.filter(user=request.user, is_watchlist=False)

    context = {
        'form': form,
        'movies': movies,
    }
    return render(request, 'diary.html', context)



@login_required
def watchlist(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user = request.user
            movie.is_watchlist = True
            movie.save()

            return redirect('watchlist')
    else:
        form = MovieForm()

    watchlist_movies = Movie.objects.filter(user=request.user, is_watchlist=True)

    context = {
        'form': form,
        'watchlist_movies': watchlist_movies,
    }

    return render(request, 'watchlist.html', context)


@login_required
def delete_movie(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    movie.delete()
    return redirect('watchlist')


@login_required
def favorites(request):
    favorite_movies = FavoriteMovie.objects.filter(user=request.user).select_related('movie')
    return render(request, 'favorites.html', {'favorite_movies': favorite_movies})

@login_required
def movie_details(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    comments = Comment.objects.filter(movie=movie).order_by('-created_at')

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.movie = movie
            comment.save()

            # Debugging: Print the username
            print("Comment user:", request.user.username)

            # Redirect to the same movie details page after posting a comment
            return redirect('movie_details', movie_id=movie_id)
    else:
        comment_form = CommentForm()

    return render(request, 'movie_details.html', {'movie': movie, 'comments': comments, 'comment_form': comment_form})

@login_required
def add_to_favorites(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    favorite_movie = FavoriteMovie.objects.filter(user=request.user, movie=movie).first()
    if favorite_movie:
        return redirect('favorites')

    favorite_movie = FavoriteMovie(user=request.user, movie=movie)
    favorite_movie.save()

    movie.is_favorite = True
    movie.save()


    return redirect('favorites')

@login_required  # This decorator ensures that the user is logged in to access the profile page
def profile_view(request, username=None):
    # Your logic for the profile view goes here
    # You can fetch user-related data or perform any other actions

    return render(request, 'profile.html', {'username': username})





