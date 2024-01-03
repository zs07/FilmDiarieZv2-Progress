from django.contrib import admin
from django.urls import path
from movie_tracker import views
from movie_tracker.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name="index"),
    path('watchlist/', watchlist, name='watchlist'),
    path('diary/', diary, name='diary'),
    path('favorites/', favorites, name='favorites'),
    path('accounts/signup/', views.signup_view, name='signup'),
    path('accounts/login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('like_review/<int:movie_id>/', like_review, name='like_review'),
    path('watchlist/delete/<int:movie_id>/', views.delete_movie, name='delete_movie'),
    path('movie_details/<int:movie_id>/', views.movie_details, name='movie_details'),
    path('add_to_favorites/<int:movie_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('add_to_top3/', views.add_to_top3, name='add_to_top3'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('timeline/<str:filter_type>/', timeline, name='timeline'),
    path('view_profile/<str:username>/', views.view_profile, name='view_profile'),  # Updated profile path
    path('follow_user/<str:username>/', follow_user, name='follow_user'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
