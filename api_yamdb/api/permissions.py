from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOnly(BasePermission):
    """Права Супера и Админа"""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )


class IsAdminOrReadOnly(BasePermission):
    """Права Супера и Админа или только чтение"""

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )


class IsAdminModeratorOwnerOrReadOnly(BasePermission):
    """Права Супера, Админа, Модера и Автора или только чтение"""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.owner == request.user
            or request.user.is_moderator
            or request.user.is_admin
            or request.user.is_superuser
        )
