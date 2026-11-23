from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import exception_handler
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from posts.models import Group, Post
from .permissions import IsAuthenticatedAuthorOrReadOnly
from .serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
)
from .viewsets import ListCreateViewSet


def jwt_exception_handler(exc, context):
    """Приводит ошибки невалидного JWT к формату спецификации."""
    if isinstance(exc, InvalidToken) and isinstance(
        context.get('view'), (TokenRefreshView, TokenVerifyView),
    ):
        exc = InvalidToken()
    return exception_handler(exc, context)


class PostViewSet(viewsets.ModelViewSet):
    """Позволяет читать публикации и даёт авторам право менять свои."""

    queryset = Post.objects.select_related('author').order_by('pk')
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Сохраняет публикацию от имени текущего пользователя."""
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Предоставляет доступ к комментариям конкретной публикации."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedAuthorOrReadOnly,)

    def get_post(self):
        """Возвращает публикацию из URL или вызывает ошибку 404."""
        return get_object_or_404(Post, pk=self.kwargs['post_id'])

    def get_queryset(self):
        """Возвращает комментарии публикации, указанной в URL."""
        return self.get_post().comments.select_related('author').order_by('pk')

    def perform_create(self, serializer):
        """Сохраняет комментарий к публикации от имени пользователя."""
        serializer.save(author=self.request.user, post=self.get_post())


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Открывает список групп и сведения о них для чтения."""

    queryset = Group.objects.order_by('pk')
    serializer_class = GroupSerializer
    permission_classes = (AllowAny,)


class FollowViewSet(ListCreateViewSet):
    """Показывает и создаёт подписки текущего пользователя."""

    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        """Возвращает подписки пользователя по возрастанию их ключей."""
        return (
            self.request.user.follows.select_related('following')
            .order_by('pk')
        )

    def perform_create(self, serializer):
        """Сохраняет подписку от имени текущего пользователя."""
        serializer.save(user=self.request.user)
