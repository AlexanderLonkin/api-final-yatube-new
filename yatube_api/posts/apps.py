from django.apps import AppConfig


class PostsConfig(AppConfig):
    """Регистрирует приложение с исходным типом первичного ключа."""

    default_auto_field = 'django.db.models.AutoField'
    name = 'posts'
