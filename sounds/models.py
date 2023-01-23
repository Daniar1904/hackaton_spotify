from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.db import models

from category.models import Genre

User = get_user_model()


class Sound(models.Model):
    # STATUS_CHOICES = (
    #     ('available', 'Доступно'),
    #     ('not available', 'Не доступно')
    # )

    owner = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='sounds')
    title = models.CharField(max_length=150)
    category = models.ForeignKey(Genre, related_name='sounds', on_delete=models.RESTRICT)
    image = models.ImageField(upload_to='images')
    # avail = models.CharField(choices=STATUS_CHOICES, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    owner = models.ForeignKey('user.CustomUser', related_name='comments',
                              on_delete=models.CASCADE)
    sound = models.ForeignKey(Sound, related_name='comments',
                             on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner} -> {self.sound} -> {self.created_at}'


class Like(models.Model):
    owner = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE,
                              related_name='liked_songs')
    sound = models.ForeignKey(Sound, on_delete=models.CASCADE,
                             related_name='likes')

    class Meta:
        unique_together = ['owner', 'sound']


class Favorites(models.Model):
    owner = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE,
                              related_name='favorite_songs')
    sound = models.ForeignKey(Sound, on_delete=models.CASCADE,
                             related_name='favorites')

    class Meta:
        unique_together = ['owner', 'sound']
