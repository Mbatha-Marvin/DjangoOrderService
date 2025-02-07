import httpx
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


class OpenIDAuthService:
    """
    Handles OpenID authentication, including token introspection.
    """

    @staticmethod
    def introspect_token(token: str) -> dict:
        """
        Validates an OpenID access token by calling the introspection endpoint.

        Args:
            token (str): The OpenID access token.

        Returns:
            dict: Token details if valid.

        Raises:
            AuthenticationFailed: If the token is invalid or expired.
        """
        data = {
            "client_id": settings.OPENID_CLIENT_ID,
            "client_secret": settings.OPENID_CLIENT_SECRET,
            "token": token,
        }

        try:
            response = httpx.post(
                settings.OPENID_INTROSPECT_URL, data=data, timeout=10.0
            )
            print(f"{response.content = }")
            response.raise_for_status()
            token_data = response.json()

            if not token_data.get("active", False):
                raise AuthenticationFailed("Invalid or expired token")

            return token_data
        except httpx.HTTPStatusError:
            raise AuthenticationFailed("Token introspection failed")
        except httpx.RequestError:
            print(f"{settings.OPENID_INTROSPECT_URL = }")
            raise AuthenticationFailed("Could not connect to OpenID server")
