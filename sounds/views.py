from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, mixins, GenericViewSet
from rest_framework import permissions, response, request, generics
from rest_framework.decorators import action
import logging


from .models import Sound, Comment, Like, Favorite
from . import serializers
from .permissions import IsAuthor, IsAuthorOrAdminOrSoundOwner, IsCommentFavouriteOwner
from .serializers import LikeSerializer, FavoriteSerializer, CommentSerializer

logger = logging.getLogger('django_logger')


class SoundViewSet(ModelViewSet):
    queryset = Sound.objects.all()
    """Выполнить/Создать"""
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.SoundListSerializer
        return serializers.SoundSerializer

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            return [permissions.IsAuthenticated(), IsAuthor()]
        return [permissions.IsAuthenticatedOrReadOnly()]


class CommentViewSet(ModelViewSet):
    logger.info('comment')
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCommentFavouriteOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class LikeMixin:
    @action(detail=True, methods=['POST'])
    def post(self, request, pk, *args, **kwargs):
        obj, _ = Like.objects.get_or_create(music_id=pk, owner=request.user)
        obj.like = not obj.like
        obj.save()
        status_ = 'Liked'
        if not obj.like:
            status_ = 'Unliked'
        return Response({'msg': status_})

class LikeAPIView(mixins.ListModelMixin, LikeMixin, GenericViewSet):
    logger.info('like')
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset


class FavouriteMixin:
    @action(detail=True, methods=['POST'])
    def post(self, request, pk, *args, **kwargs):
        obj, _ = Favorite.objects.get_or_create(music_id=pk, owner=request.user)
        obj.save()
        status_ = 'Добавлено'
        return Response({'msg': status_})


class FavoriteAPIView(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, FavouriteMixin,
                       GenericViewSet):
    logger.info('favorite')
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsCommentFavouriteOwner]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset