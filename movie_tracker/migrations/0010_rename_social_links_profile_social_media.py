# Generated by Django 5.0 on 2023-12-29 22:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie_tracker', '0009_remove_profile_location_remove_profile_preferences_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='social_links',
            new_name='social_media',
        ),
    ]
