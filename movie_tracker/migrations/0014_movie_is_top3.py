# Generated by Django 5.0 on 2023-12-31 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_tracker', '0013_remove_profile_followers_remove_profile_following_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='is_top3',
            field=models.BooleanField(default=False),
        ),
    ]
