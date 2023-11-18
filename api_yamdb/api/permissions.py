from rest_framework import permissions

from reviwes.models import User


class ReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS


class ReadOnlyOrAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.method in permissions.SAFE_METHODS
                    or (request.user
                        and request.user.is_authenticated
                        and request.user.role == User.ADMIN
                        )
                    )