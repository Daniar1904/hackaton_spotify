from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models

from category.models import Genre

User = get_user_model()


class Sound(models.Model):
    """Подготавливаем модели наших треков"""
    owner = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='sounds')
    title = models.CharField(max_length=150)
    """В file используем функцию добавления музыкального файла по расширению mp3"""
    file = models.FileField(
        upload_to='songs',
        validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav'])], blank=True
    )
    singer = models.CharField(max_length=50, blank=True)
    category = models.ForeignKey(Genre, related_name='sounds', on_delete=models.RESTRICT)
    cover = models.ImageField(upload_to='covers', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Создаем класс для добавления комментариев/отзывов"""
    owner = models.ForeignKey('user.CustomUser', related_name='comments',
                              on_delete=models.CASCADE)
    sound = models.ForeignKey(Sound, related_name='comments',
                             on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner} -> {self.sound} -> {self.created_at}'


class Like(models.Model):
    """Создаем класс для лайков"""
    owner = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE,
                              related_name='liked_songs')
    sound = models.ForeignKey(Sound, on_delete=models.CASCADE,
                             related_name='likes')

    class Meta:
        unique_together = ['owner', 'sound']


class Favorites(models.Model):
    """Создаем класс для добавления пользователем продукта в избранные"""
    owner = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE,
                              related_name='favorite_songs')
    sound = models.ForeignKey(Sound, on_delete=models.CASCADE,
                             related_name='favorites')

    class Meta:
        unique_together = ['owner', 'sound']
