from django.contrib import admin
from django.urls import path
from movie_tracker import views
from movie_tracker.views import watchlist, diary, favorites
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
    path('watchlist/delete/<int:movie_id>/', views.delete_movie, name='delete_movie'),
    path('movie_details/<int:movie_id>/', views.movie_details, name='movie_details'),
    path('add_to_favorites/<int:movie_id>/', views.add_to_favorites, name='add_to_favorites'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


