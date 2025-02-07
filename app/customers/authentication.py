from .services.auth_service import OpenIDAuthService
from rest_framework.authentication import BaseAuthentication


class OpenIDUser:
    """A lightweight user-like object for OpenID authentication."""

    def __init__(self, user_data: dict) -> None:
        self.user_data = user_data
        self.username = user_data.get("preferred_username", "unknown")
        self.is_authenticated = True

    def __str__(self) -> str:
        return self.username


class OpenIDAuthentication(BaseAuthentication):
    """Django authentication class using OpenID authentication."""

    def authenticate(self, request):
        """
        Extracts the OpenID token and validates it using OpenIDAuthService.

        Args:
            request: The incoming Django request.

        Returns:
            A tuple (OpenIDUser, None) if authentication is successful.

        Raises:
            AuthenticationFailed: If token is invalid.
        """
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None  # No token provided

        token = auth_header.split(" ")[1]
        token_data = OpenIDAuthService.introspect_token(token)
        return OpenIDUser(token_data), None
