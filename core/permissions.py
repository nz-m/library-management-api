from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """
    Permission class for checking if the user is an admin.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.account_type == 'administrator'


class IsRegularUser(BasePermission):
    """
    Permission class for checking if the user is a regular member.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.account_type == 'regular'
