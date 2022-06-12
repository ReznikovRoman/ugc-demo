from aiohttp import web


async def index(request):
    return web.Response(text="Home page!")


async def create_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/", index)
    return app
