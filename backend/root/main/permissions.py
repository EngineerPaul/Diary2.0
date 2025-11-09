from rest_framework import permissions


class CustomPermission(permissions.BasePermission):
    """ Authorized only """

    def has_permission(self, request, view):
        if request.user_info['is_auth'] is True:
            return True
        return False
