from rest_framework.permissions import BasePermission, SAFE_METHODS
# from rest_framework import permissions

# from reviwes.models import User


# class ReadOnly(permissions.BasePermission):

#     def has_object_permission(self, request, view, obj):
#         return request.method in permissions.SAFE_METHODS


# class ReadOnlyOrAdminUser(permissions.BasePermission):

#     def has_permission(self, request, view):
#         return bool(request.method in permissions.SAFE_METHODS
#                     or (request.user
#                         and request.user.is_authenticated
#                         and request.user.role == User.ADMIN
#                         )
#                     )
    

class IsAdminOnly(BasePermission):
    """Права Супера и Админа (как ReadOnly)"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(BasePermission):
    """Права Супера и Админа или только чтение (безопасные запросы) (как ReadOnlyOrAdminUser)"""

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )


class IsAdminModeratorOwnerOrReadOnly(BasePermission):
    """Права Супера, Админа, Модера и Автора или только чтение (безопасные запросы)"""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.owner == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )