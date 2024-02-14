import falcon.asgi
import uvicorn
from middlewares.authenticate import AuthenticateMiddleware
from middlewares.proxy import ProxyMiddleware


async def sink(req, resp):
    pass


def get_app() -> falcon.API:
    app = falcon.asgi.App(middleware=falcon.CORSMiddleware(
        allow_origins='http://localhost:9000', allow_credentials='*'))
    app.add_middleware(
        middleware=[ProxyMiddleware()])
    app.add_sink(sink)
    return app


if __name__ == '__main__':
    uvicorn.run(get_app(), port=8001)
