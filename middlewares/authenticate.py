import falcon
from middlewares.proxy import options_request, proxy_request
import constants


USER_PATHS = ['/api/user/login/', '/api/user/logout/', '/api/user/']

class AuthenticateMiddleware:
    user_paths = USER_PATHS

    @options_request
    @proxy_request(target_url=constants.USER_SERVICE_HOST, paths=user_paths)
    async def process_request(self, req: falcon.Request, resp: falcon.Response):
        pass
