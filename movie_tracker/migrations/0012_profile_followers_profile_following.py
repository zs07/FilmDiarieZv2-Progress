# Generated by Django 5.0 on 2023-12-30 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_tracker', '0011_alter_profile_recently_viewed_movies'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='followers_profiles', to='movie_tracker.profile'),
        ),
        migrations.AddField(
            model_name='profile',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='following_profiles', to='movie_tracker.profile'),
        ),
    ]
