# Generated by Django 4.2.1 on 2023-05-26 08:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_name', models.CharField(max_length=255)),
                ('details', models.CharField(max_length=200)),
                ('poster', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('rating', models.FloatField()),
                ('review', models.TextField()),
                ('is_watchlist', models.BooleanField(default=False)),
                ('is_favorite', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
