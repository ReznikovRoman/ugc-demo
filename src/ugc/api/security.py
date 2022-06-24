from typing import Any, Final, Mapping
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from jose import JWTError, jwt

from ugc.common.exceptions import AuthorizationError
from ugc.containers import Container

TOKEN_TYPE: Final[str] = "Bearer"


def get_token_from_header(headers: Mapping[str, Any]) -> str:
    """Получение токена из заголовка 'Authorization'."""
    auth = headers.get("Authorization", None)
    if not auth:
        raise AuthorizationError("Authorization header is expected", "authorization_header_missing")

    parts = auth.split()
    if parts[0].lower() != TOKEN_TYPE.lower():
        raise AuthorizationError(f"Authorization header must start with {TOKEN_TYPE}", "invalid_header")
    if len(parts) == 1:
        raise AuthorizationError("Token not found", "invalid_header")
    if len(parts) > 2:
        raise AuthorizationError(f"Authorization header must be {TOKEN_TYPE} token", "invalid_header")

    token = parts[1]
    return token


@inject
def get_user_id_from_jwt(headers: Mapping[str, Any], config=Provide[Container.config]) -> UUID:
    """Получение id пользователя из JWT токена."""
    token = get_token_from_header(headers)
    try:
        payload = jwt.decode(token, config["JWT_AUTH_SECRET_KEY"], algorithms=[config["JWT_AUTH_ALGORITHM"]])
        user_id: str = payload.get("sub")
    except JWTError:
        raise AuthorizationError
    return UUID(user_id)
