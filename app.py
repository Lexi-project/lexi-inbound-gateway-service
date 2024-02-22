import falcon
import falcon.asgi
import uvicorn
import constants

from middlewares.authenticate import AuthenticateMiddleware
from middlewares.proxy import ProxyMiddleware


async def sink(req: falcon.Request, resp: falcon.Response):
    pass


def get_app() -> falcon.API:
    app = falcon.asgi.App(middleware=falcon.CORSMiddleware(
        allow_origins=constants.CORS_ALLOWED_ORIGINS, allow_credentials='*'))
    app.add_middleware(
        middleware=[AuthenticateMiddleware(), ProxyMiddleware()])
    app.add_sink(sink)
    return app


if __name__ == '__main__':
    uvicorn.run(get_app(), port=8001)
