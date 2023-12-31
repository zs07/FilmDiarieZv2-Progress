from django.contrib import admin
from django.urls import path
from movie_tracker import views
from movie_tracker.views import watchlist, diary, favorites, like_review, movie_details
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
    path('profile/<str:username>/', views.profile_view, name='profile'), # Added profile path
    path('like_review/<int:movie_id>/', like_review, name='like_review'),
    path('watchlist/delete/<int:movie_id>/', views.delete_movie, name='delete_movie'),
    path('movie_details/<int:movie_id>/', views.movie_details, name='movie_details'),
    path('add_to_favorites/<int:movie_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('add_to_top3/', views.add_to_top3, name='add_to_top3'),
    path('delete_account/', views.delete_account, name='delete_account'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
