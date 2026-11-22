from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import (
    TokenRefreshSerializer,
    TokenVerifySerializer,
)


class TokenErrorResponseMixin:
    def validate(self, attrs):
        try:
            return super().validate(attrs)
        except TokenError as error:
            raise InvalidToken() from error


class JWTRefreshSerializer(TokenErrorResponseMixin, TokenRefreshSerializer):
    pass


class JWTVerifySerializer(TokenErrorResponseMixin, TokenVerifySerializer):
    pass
