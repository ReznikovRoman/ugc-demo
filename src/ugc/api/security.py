from jose import JWTError, jwt

from aiohttp import web

from ugc.core.config import get_settings

settings = get_settings()


def get_jwt_token(request) -> str:
    """Получение JWT токена из заголовка."""
    token = request.headers.get("Authorization", None)
    if token:
        return token
    raise web.HTTPUnauthorized(reason="Authorization needed")


def get_user_id(request) -> str:
    """Получение id пользователя из JWT токена."""
    token = get_jwt_token(request)
    try:
        payload = jwt.decode(token, settings.JWT_AUTH_SECRET_KEY, algorithms=[settings.JWT_AUTH_ALGORITHM])
        user_id: str = payload.get("sub")
    except JWTError:
        raise web.HTTPUnauthorized(reason="invalid JWT")
    return user_id
