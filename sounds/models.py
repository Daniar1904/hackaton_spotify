from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


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
    # preview = models.ImageField(upload_to='images/', null=True)
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
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    sound = models.ForeignKey(Sound, on_delete=models.CASCADE, related_name='likes')
    like = models.BooleanField(default=False)


class Favorite(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    sound = models.ForeignKey(Sound, on_delete=models.CASCADE, related_name='favorites', null=True, blank=True)
