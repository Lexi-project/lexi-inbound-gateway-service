import falcon


class HealthcheckResource:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
