import falcon
from middlewares.proxy import options_request, proxy_request


class AuthenticateMiddleware:
    user_paths = ['/api/user/login/', '/api/user/logout/', '/api/user/']

    @options_request
    @proxy_request(target_url='http://localhost:9002', paths=user_paths)
    async def process_request(self, req: falcon.Request, resp: falcon.Response):
        pass
