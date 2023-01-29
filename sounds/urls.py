

from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter, DefaultRouter

from .views import CommentViewSet, LikeAPIView, FavoriteAPIView


"""Прописываем пути нашим атрибутам(комментариям, лайкам, подпискам)"""

router = DefaultRouter()
router.register('comment', CommentViewSet)
router.register('like', LikeAPIView)
router.register('favorite', FavoriteAPIView)

urlpatterns = [
    path('', include(router.urls))
]