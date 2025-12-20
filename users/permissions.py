from rest_framework.permissions import BasePermission


class IsAdminOrSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.id == request.user.id

    def has_permission(self, request, view):

        if request.method == "GET" and not view.kwargs.get("id"):
            return request.user.is_staff

        if request.method in ["POST", "DELETE"]:
            return request.user.is_staff

        return True
