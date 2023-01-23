from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, response, request, generics
from rest_framework.decorators import action

from user.views import StandartResultPagination
from .models import Sound, Comment, Like
from . import serializers
from .permissions import IsAuthor, IsAuthorOrAdminOrPostOwner


class SoundViewSet(ModelViewSet):
    queryset = Sound.objects.all()

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


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH'):
            return [permissions.IsAuthenticated(), IsAuthor()]
        elif self.request.method == 'DELETE':
            return [permissions.IsAuthenticated(),
                    IsAuthorOrAdminOrPostOwner()]
        return [permissions.AllowAny()]

class LikeCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.LikeSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeDeleteView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsAuthor)


class FollowedUsersPostsView(generics.ListAPIView):
    queryset = Sound.objects.all()
    serializer_class = serializers.SoundListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = StandartResultPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        followings = request.user.followers.all()
        users = [user.following for user in followings]
        res = queryset.filter(owner__in=users)
        serializer = serializers.SoundListSerializer(
            instance=res, many=True, context={'request': request})
        return Response(serializer.data, status=200)