from django.contrib import admin

from sounds.models import Sound, Comment, Like, Favorite

admin.site.register(Sound)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Favorite)