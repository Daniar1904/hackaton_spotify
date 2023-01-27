from django.contrib import admin
from .models import Genre, Favorites, Like, Comment
from sounds.models import Sound

admin.site.register(Sound)
admin.site.register(Genre)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Favorites)
