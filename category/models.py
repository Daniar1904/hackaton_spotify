from django.db import models

from sounds.models import Sound
from user.models import CustomUser


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Album(models.Model):
    """ Модель альбомов для треков
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='albums')
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    private = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to='covers_of_albums',
        blank=True,
        null=True,
    )


class PlayList(models.Model):
    """ Модель плейлистов пользователя
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='play_lists')
    title = models.CharField(max_length=50)
    song = models.ManyToManyField(Sound, related_name='songs_play_lists')
    cover = models.ImageField(
        upload_to='covers_of_playlists',
        blank=True,
        null=True,
    )


