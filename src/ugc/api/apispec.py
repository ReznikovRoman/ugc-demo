from aiohttp_apispec import setup_aiohttp_apispec, validation_middleware

from aiohttp import web


def init_apispec(app: web.Application) -> None:
    setup_aiohttp_apispec(
        app=app,
        title="Netflix UGC",
        version="v1",
        url="/docs/swagger.json",
        swagger_path="/docs",
        securityDefinitions={
            "JWT": {
                "type": "apiKey",
                "in": "header",
                "name": "Authorization",
                "description": "В поле *'Value'* надо вставить JWT: **'Bearer &lt;JWT&gt;'**, JWT - токен авторизации",
            },
        },
    )
    app.middlewares.append(validation_middleware)
