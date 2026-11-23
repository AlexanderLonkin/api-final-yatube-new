from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly


class IsAuthenticatedAuthorOrReadOnly(IsAuthenticatedOrReadOnly):
    """Разрешает чтение всем, а запись только автору после входа."""

    def has_object_permission(self, request, view, obj):
        """Разрешает безопасные методы и даёт автору право на запись."""
        return request.method in SAFE_METHODS or obj.author == request.user
