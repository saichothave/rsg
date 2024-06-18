from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin users to edit it.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        print('request', request.user)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the admin user.
        return request.user and request.user.is_staff
