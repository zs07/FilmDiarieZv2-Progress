# Generated by Django 5.0 on 2023-12-30 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_tracker', '0012_profile_followers_profile_following'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='followers',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='following',
        ),
        migrations.AddField(
            model_name='profile',
            name='follows',
            field=models.ManyToManyField(blank=True, related_name='followed_by', to='movie_tracker.profile'),
        ),
    ]
