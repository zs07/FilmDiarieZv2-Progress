import re
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.forms import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.http import JsonResponse, HttpResponseServerError
from django.db.models import Q
from .forms import *
from .models import *

# User registration view
def signup_view(request):
    if request.method == "POST":
        username, email, password = request.POST["username"], request.POST["email"], request.POST["password"]
        bio, social_media_links = request.POST.get('bio'), request.POST.get('social_media')

        # Check username format
        if not re.match("^[a-zA-Z0-9_]+$", username):
            return render(request, "signup.html", {"message": "Invalid username format. Use only letters, numbers, and underscores."})

        try:
            # Create user and associated profile
            user = User.objects.create_user(username=username, email=email, password=password)
            Profile.objects.create(user=user, bio=bio, social_media=social_media_links.split(','))

        except IntegrityError:
            return render(request, "signup.html", {"message": "Username is already taken. Please choose a different one."})

        except ValidationError:
            return render(request, "signup.html", {"message": "Email address is already registered."})

        # Log in user and redirect
        login(request, user)
        return redirect("index")

    return render(request, "signup.html")

# User login view
def login_view(request):
    if request.method == "POST":
        username, password = request.POST.get("username"), request.POST.get("password")

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log in user and redirect
            login(request, user)
            return redirect("index")
        else:
            return render(request, "login.html", {"message": "Invalid credentials."})

    return render(request, "login.html")

# User logout view
def logout_view(request):
    logout(request)
    return redirect("login")

# Home page view
def index(request):
    return render(request, "base.html")

# User diary view
@login_required
@transaction.atomic
def diary(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            # Save movie entry and handle favorites
            movie = form.save(commit=False)
            movie.user = request.user
            movie.is_watchlist = False

            if form.cleaned_data['is_favorite']:
                movie.is_favorite = True

            if Movie.objects.filter(user=request.user, movie_name=movie.movie_name).exists():
                return redirect('diary')

            movie.save()

            if movie.is_favorite:
                favorite_movie = FavoriteMovie(user=request.user, movie=movie)
                favorite_movie.save()

                return redirect('diary')

    # Retrieve user's diary entries
    movies = Movie.objects.filter(user=request.user, is_watchlist=False, is_top3=False).order_by('-date').select_related('user')

    context = {'movies': movies}
    return render(request, 'diary.html', context)

# User watchlist view
@login_required
def watchlist(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            # Save watchlist entry
            movie = form.save(commit=False)
            movie.user = request.user
            movie.is_watchlist = True
            movie.save()

            return redirect('watchlist')
    else:
        form = MovieForm()

    # Retrieve user's watchlist entries
    watchlist_movies = Movie.objects.filter(user=request.user, is_watchlist=True)

    context = {'form': form, 'watchlist_movies': watchlist_movies}
    return render(request, 'watchlist.html', context)

# Add movie to user's top 3 view
@login_required
def add_to_top3(request):
    if request.method == 'POST':
        # Check and add movie to top 3
        movie_name, details, poster = request.POST.get('movie_name'), request.POST.get('details'), request.POST.get('poster')

        profile = Profile.objects.get(user=request.user)

        if profile.top3_movies.count() >= 3:
            return render(request, 'profile.html', {'error_message': "You can have at most three movies in your top 3."})

        if not profile.top3_movies.filter(movie_name=movie_name).exists():
            movie = Movie.objects.create(
                user=request.user,
                movie_name=movie_name,
                details=details,
                poster=poster,
                is_watchlist=False,
                is_favorite=False,
                is_top3=True,
            )
            profile.top3_movies.add(movie)

    return redirect('profile')

# Delete movie from user's entries view
@login_required
def delete_movie(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    movie.delete()

    # Redirect back to the referring page or watchlist
    referer_url = request.META.get('HTTP_REFERER', None)

    if referer_url and referer_url.startswith(request.build_absolute_uri('/')[:-1]):
        return redirect(referer_url)
    else:
        return redirect('watchlist')

# User favorite movies view
@login_required
def favorites(request):
    # Retrieve user's favorite movies
    favorite_movies = FavoriteMovie.objects.filter(user=request.user).select_related('movie')
    return render(request, 'favorites.html', {'favorite_movies': favorite_movies})

# Movie details view
@login_required
def movie_details(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    comments = Comment.objects.filter(movie=movie).order_by('-created_at')

    if request.method == 'POST':
        # Save comment and create notifications
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.movie = movie
            comment.save()

            Notification.objects.create(
                notification_type='C',
                sender=request.user,
                receiver=movie.user,
                comment=comment,
            )

            return redirect('movie_details', movie_id=movie_id)
    else:
        comment_form = CommentForm()

    return render(request, 'movie_details.html', {'movie': movie, 'comments': comments, 'comment_form': comment_form})

# Add movie to user's favorites view
def add_to_favorites(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    favorite_movie, created = FavoriteMovie.objects.get_or_create(user=request.user, movie=movie)

    if created:
        movie.is_favorite = True
        movie.save()

    return redirect('favorites')

# User profile view
@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    all_time_favorites = profile.all_time_favorites.all()

    recent_activity = Movie.objects.filter(
        Q(user=request.user, is_watchlist=False) & ~Q(id__in=profile.top3_movies.all())
    ).order_by('-date')[:5]

    diary_movies = Movie.objects.filter(
        user=request.user,
        is_watchlist=False,
        is_top3=False
    ).exclude(id__in=profile.top3_movies.all())

    films_count = diary_movies.count()
    notifications = Notification.objects.filter(receiver=request.user).order_by('-created_at')[:10]
    top3_movies = profile.top3_movies.all()
    profile_movies = Movie.objects.filter(user=request.user, is_watchlist=False)
    bio = profile.bio
    social_media = profile.social_media
    following_count = profile.following.count()
    followers_count = profile.followers.count()
    profile_picture_url = profile.profile_picture.url if profile.profile_picture else None

    context = {
        'user': request.user,
        'all_time_favorites': all_time_favorites,
        'recent_activity': recent_activity,
        'top3_movies': top3_movies,
        'films_count': films_count,
        'following_count': following_count,
        'followers_count': followers_count,
        'bio': bio,
        'social_media': social_media,
        'profile_picture_url': profile_picture_url,
        'notifications': notifications,
    }

    return render(request, 'profile.html', context)

# User account deletion view
@login_required
def delete_account(request):
    user = request.user
    user.delete()
    return redirect('home')

# Update user profile view
@login_required
def update_profile(request):
    if request.method == 'POST':
        bio, social_media, profile_picture = request.POST.get('bio'), request.POST.get('social_media'), request.FILES.get('profile_picture')
        profile = Profile.objects.get(user=request.user)

        if bio is not None:
            profile.bio = bio
        if social_media is not None:
            profile.social_media = social_media.split(',') if social_media else []
        if profile_picture is not None:
            profile.profile_picture = profile_picture

        profile.save()

        return JsonResponse({
            'bio': profile.bio,
            'social_media': profile.social_media,
            'profile_picture_url': profile.profile_picture.url,
        })

# Movie review like/unlike view
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def like_review(request, movie_id):
    try:
        movie = get_object_or_404(Movie, id=movie_id)
        user = request.user
        favorite_movie = FavoriteMovie.objects.filter(user=user, movie=movie).first()

        if favorite_movie:
            favorite_movie.delete()
            movie.review_likes -= 1
            liked = False
        else:
            FavoriteMovie.objects.create(user=user, movie=movie)
            movie.review_likes += 1
            liked = True

        movie.save()

        # Create a notification for the original reviewer
        if movie.review and hasattr(movie.review, 'user'):
            Notification.objects.create(
                notification_type='L',
                sender=request.user,
                receiver=movie.review.user,
                movie=movie.review.movie,
            )

        # Create a notification for the movie owner
        if user != movie.user:
            Notification.objects.create(
                notification_type='L',
                sender=request.user,
                receiver=movie.user,
                movie=movie,
            )

        return JsonResponse({'review_likes': movie.review_likes, 'liked': liked})
    except Exception as e:
        print(f"Error in like_review view: {e}")
        return JsonResponse({'error': 'Error occurred while processing the like.'}, status=500)

# User activity timeline view
@login_required
def timeline(request, filter_type='all'):
    user = request.user
    entries = []

    if filter_type == 'friends':
        # Display activity of people the user is following
        following_users = user.profile.following.values_list('user__id', flat=True)
        entries = Movie.objects.filter(
        Q(user__id__in=following_users, is_watchlist=False, is_top3=False)
        ).order_by('-date').select_related('user')

    elif filter_type == 'all':
        # Display all activity
        entries = Movie.objects.filter(
            is_watchlist=False, is_top3=False
        ).order_by('-date').select_related('user')

    context = {'entries': entries, 'filter_type': filter_type}
    return render(request, 'home_timeline.html', context)

# View other user's profile
@login_required
def view_profile(request, username):
    if request.user.username == username:
        # If the requested username is the same as the logged-in user, redirect to their own profile
        return redirect('profile')

    other_user_profile = get_object_or_404(Profile.objects.select_related('user').prefetch_related('top3_movies'), user__username=username)

    # Additional data retrieval for the user being viewed
    other_user_recent_activity = Movie.objects.filter(
        Q(user=other_user_profile.user, is_watchlist=False) & ~Q(id__in=other_user_profile.top3_movies.all())
    ).order_by('-date')[:5].values('poster', 'movie_name')  # Select only necessary fields

    other_user_top3_movies = other_user_profile.top3_movies.values('poster', 'movie_name')  # Select only necessary fields

    # Calculate counts
    films_count = Movie.objects.filter(user=other_user_profile.user, is_watchlist=False, is_top3=False).count()
    view_following_count = other_user_profile.following.count()
    view_followers_count = other_user_profile.followers.count()

    context = {
        'other_user_profile': other_user_profile,
        'other_user_recent_activity': other_user_recent_activity,
        'other_user_top3_movies': other_user_top3_movies,
        'films_count': films_count,
        'following_count': view_following_count,
        'followers_count': view_followers_count,
    }

    return render(request, 'view_profile.html', context)

# Follow/unfollow user view
@login_required
@transaction.atomic
def follow_user(request, username):
    try:
        other_user = get_object_or_404(User, username=username)
        other_user_profile = Profile.objects.get(user=other_user)
        logged_in_user_profile = Profile.objects.get(user=request.user)

        if request.user in other_user_profile.followers.all():
            # If already following, unfollow
            logged_in_user_profile.following.remove(other_user_profile)
            other_user_profile.followers.remove(request.user)
        else:
            # If not following, follow
            logged_in_user_profile.following.add(other_user_profile)
            other_user_profile.followers.add(request.user)

        # Save changes to the database
        logged_in_user_profile.save()
        other_user_profile.save()
        # Create a follow notification
        Notification.objects.create(
            notification_type='F',
            sender=request.user,
            receiver=other_user,
        )

        # Redirect back to the profile page
        return redirect('view_profile', username=username)

    except Exception as e:
        print(f"Error in follow_user view: {e}")
        return HttpResponseServerError("Internal Server Error")
