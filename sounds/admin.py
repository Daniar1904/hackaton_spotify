from django.contrib import admin

from sounds.models import Sound, Comment, Like, Favorite, Genre

admin.site.register(Sound)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Favorite)
admin.site.register(Genre)
