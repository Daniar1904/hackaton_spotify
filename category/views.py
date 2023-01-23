from django.shortcuts import render
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from category import serializers
from category.models import Genre


class CategoryViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = serializers.CategorySerializer

    def get_permissions(self):
        if self.action in ('retrieve', 'list'):
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAdminUser()]
