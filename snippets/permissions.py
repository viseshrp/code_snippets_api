from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    All snippets are visible to everyone.(read only)
    But only the owner can write. (read write)
    """

    def has_object_permission(self, request, view, obj):
        # allow all 'safe' request methods - GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True

        # obj - snippet object
        # return true if object owner is the same as requesting user.
        return obj.owner == request.user
