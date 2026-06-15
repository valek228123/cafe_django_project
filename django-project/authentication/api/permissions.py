from rest_framework import permissions


class AdminAndUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return request.user and  request.user.is_authenticated and request.user.is_staff
        else:
            return True
