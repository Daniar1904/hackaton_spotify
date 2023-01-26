from rest_framework import permissions

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
class IsAuthorOrAdminOrPostOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        elif request.user == obj.post.owner:
            return True
        return request.user == obj.owner