import falcon
from wsgiref.simple_server import make_server

from resources.health_check import HealthcheckResource


def get_app() -> falcon.API:
    app = falcon.App()
    app.add_route('/health-check', HealthcheckResource())
    return app


if __name__ == '__main__':
    with make_server('', 8000, get_app()) as httpd:
        print('Serving on port 8000...')
        httpd.serve_forever()
