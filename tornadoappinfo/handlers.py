"""App Info handler."""
from tornado.web import RequestHandler
from tornado.httpclient import AsyncHTTPClient
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
            dep_requests = {dep: self.client.fetch(url)
                            for dep, url in app.info_dependencies.items()}
            deps = yield dep_requests
            deps = {dep: json_decode(resp.body) for dep, resp in deps.items()}
            info['dependencies'] = deps

        self.write(json_encode(info))
