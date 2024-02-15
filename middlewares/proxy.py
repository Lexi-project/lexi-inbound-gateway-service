import json
import httpx
import falcon


def options_request(func):
    async def wrapper(self, req: falcon.Request, resp: falcon.Response):
        if req.method == 'OPTIONS':
            resp.status = falcon.HTTP_200
            return
        await func(self, req, resp)
    return wrapper

def authenticate(paths: list[str]=[]):
    def decorator(func):
        async def wrapper(self, req: falcon.Request, resp: falcon.Response):
            if req.path in paths:
                headers = {k: v for k, v in req.headers.items() if k.lower()
                            != 'content-length'}
                auth_header = req.headers.get('authorization', '')
                headers['authorization'] = f'Bearer {auth_header}'
                async with httpx.AsyncClient(headers=headers) as client:
                    response = await client.request(
                        'GET',
                        'http://localhost:9002/api/user/'
                    )
                    user = json.loads(response.content)
                    user_id = user.get('user_id', None)
                    if response.status_code != 200 or not user_id:
                        resp.status = falcon.HTTP_401
                        return
                    req.headers['x-user-id'] = str(user_id)
            await func(self, req, resp)
        return wrapper
    return decorator


def proxy_request(target_url: str, paths: list[str]=[]):
    def decorator(func):
        async def wrapper(self, req: falcon.Request, resp: falcon.Response):
            if len(paths) == 0 or req.path in paths:
                async with httpx.AsyncClient(headers=req.headers) as client:
                    async with client.stream(
                        req.method,
                        f'{target_url}{req.path}',
                        data=req.stream,
                    ) as response:
                        resp.text = b''
                        async for chunk in response.aiter_bytes():
                            resp.text += chunk
            await func(self, req, resp)
        return wrapper
    return decorator


class ProxyMiddleware:

    @options_request
    @authenticate(paths=['/'])
    @proxy_request(target_url='http://localhost:4000/graphql', paths=['/'])
    async def process_request(self, req: falcon.Request, resp: falcon.Response):
        pass
