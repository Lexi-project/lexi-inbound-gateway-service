import json
import httpx
import falcon


def options_request(func):
    async def wrapper(self, req, resp):
        if req.method == 'OPTIONS':
            resp.status = falcon.HTTP_200
            return
        await func(self, req, resp)
    return wrapper


def authenticate(func):
    async def wrapper(self, req, resp):
        async with httpx.AsyncClient() as client:
            headers = {k: v for k, v in req.headers.items() if k.lower()
                       != 'content-length'}
            auth_header = req.headers.get('authorization', '')
            headers['authorization'] = f'Bearer {auth_header}'
            response = await client.request(
                'GET',
                'http://localhost:9002/api/user/',
                headers=headers,
            )
            user = json.loads(response.content)
            user_id = user.get('user_id', None)
            if response.status_code != 200 or not user_id:
                resp.status = falcon.HTTP_401
                return
            req.headers['x-user-id'] = str(user_id)
        await func(self, req, resp)
    return wrapper


def proxy_request(target_url, paths=[]):
    def decorator(func):
        async def wrapper(self, req, resp):
            if len(paths) == 0 or req.path in paths:
                async with httpx.AsyncClient() as client:
                    request_data = await req.stream.read()
                    response = await client.request(
                        req.method,
                        f'{target_url}{req.path}',
                        headers={**req.headers},
                        content=request_data,
                    )
                    resp.status = response.status_code
                    resp.headers.update(response.headers)
                    resp.data = response.content
                    resp.complete = True
            await func(self, req, resp)
        return wrapper
    return decorator


class ProxyMiddleware:

    @options_request
    @authenticate
    @proxy_request(target_url='http://localhost:4000/graphql', paths=['/'])
    async def process_request(self, req, resp):
        pass
