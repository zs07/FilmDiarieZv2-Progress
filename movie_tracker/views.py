from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import MovieForm
from django.db import IntegrityError
from .models import Movie, FavoriteMovie



def signup_view(request):
    if request.method == "POST":
        full_name = request.POST["full_name"].split(" ")
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            user = User.objects.create_user(username=email, email=email, password=password,
                                            first_name=full_name[0], last_name=full_name[-1])
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
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)
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
    return render(request, 'movie_details.html', {'movie': movie})

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





