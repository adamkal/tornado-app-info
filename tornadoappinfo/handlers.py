"""App Info handler."""
from tornado.web import RequestHandler
from tornado.httpclient import AsyncHTTPClient, HTTPError
from tornado.escape import json_encode, json_decode
from tornado import gen


class InfoHandler(RequestHandler):

    def initialize(self):
        self.client = AsyncHTTPClient()

    @gen.coroutine
    def get(self):
        app = self.application
        info = app.info

        if app.info_dependencies is not None:
            info['dependencies'] = yield self._get_dependencies()

        self.write(json_encode(info))

    @gen.coroutine
    def _get_dependencies(self):
        app = self.application
        deps = {}

        dep_requests = {dep: self.client.fetch(url)
                        for dep, url in app.info_dependencies.items()}

        for dep, req in dep_requests.items():
            try:
                resp = yield req
            except HTTPError as e:
                resp = e.response
                deps[dep] = {
                    'code': resp.code,
                    'error': resp.body.decode()
                }
            else:
                deps[dep] = json_decode(resp.body)

        raise gen.Return(deps)
