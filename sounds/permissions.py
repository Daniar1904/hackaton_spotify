from rest_framework import permissions
from rest_framework.permissions import BasePermission

"""Прописываем ограничения для изменения и добавления треков"""
class IsAuthorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return request.user == obj.owner


"""Ограничения на добавления изменений автором"""
class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


"""Ограничение на добавление изменений автором или админом"""
class IsAuthorOrAdminOrSoundOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        elif request.user == obj.post.owner:
            return True
        return request.user == obj.owner



class IsCommentFavouriteOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH']:
            return request.user.is_authenticated and request.user == obj.owner
        return request.user.is_authenticated and request.user == obj.owner