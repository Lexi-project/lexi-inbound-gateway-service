from middlewares.proxy import proxy_request


class AuthenticateMiddleware:
    user_paths = ['/api/user/login/', '/api/user/logout/', '/api/user/']

    @proxy_request(target_url='http://localhost:9002', paths=user_paths)
    async def process_request(self, req, resp):
        pass
