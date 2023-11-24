from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOnly(BasePermission):
    """Права Супера и Админа"""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.is_admin
        )


class IsAdminOrReadOnly(IsAdminOnly):
    """Права Супера и Админа или только чтение"""

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or super().has_permission(request, view)
        )


class IsAdminModeratorOwnerOrReadOnly(IsAdminOrReadOnly):
    """Права Супера, Админа, Модера и Автора или только чтение"""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            super().has_permission(request, view)
            or obj.owner == request.user
            or request.user.is_moderator
        )
