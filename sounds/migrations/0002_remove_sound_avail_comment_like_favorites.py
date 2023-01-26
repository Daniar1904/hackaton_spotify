# Generated by Django 4.1.5 on 2023-01-24 13:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sounds', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sound',
            name='avail',
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('sound', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='sounds.sound')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_songs', to=settings.AUTH_USER_MODEL)),
                ('sound', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='sounds.sound')),
            ],
            options={
                'unique_together': {('owner', 'sound')},
            },
        ),
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_songs', to=settings.AUTH_USER_MODEL)),
                ('sound', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='sounds.sound')),
            ],
            options={
                'unique_together': {('owner', 'sound')},
            },
        ),
    ]
