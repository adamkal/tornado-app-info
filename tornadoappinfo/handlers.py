"""App Info handler."""

import logging

import six
from tornado.web import RequestHandler
from tornado.httpclient import AsyncHTTPClient, HTTPError
from tornado.escape import json_encode, json_decode
from tornado import gen

str = six.text_type

log = logging.getLogger('tornadoappinfo.handlers')


class InfoHandler(RequestHandler):

    def initialize(self):
        self.client = AsyncHTTPClient()

    @gen.coroutine
    def get(self):
        app = self.application
        info = app.info
        deps = app.info_dependencies

        log.debug("Getting application information from {} collectors "
                  "and {} dependent services.".format(len(app.info),
                                                      len(deps or {})))

        if deps is not None:
            info['dependencies'] = yield self._get_dependencies()

        self.write(json_encode(info))

    @gen.coroutine
    def _get_dependencies(self):
        app = self.application
        deps = {}

        for dep, url in app.info_dependencies.items():

            log.info(
                "Fetching info about '{}' service @ '{}'".format(dep, dep))

            try:
                resp = yield self.client.fetch(url)
            except HTTPError as http_err:

                log.error(
                    "Dependent service '{}' error @ '{}': {}"
                    "".format(dep, url, http_err))

                resp = http_err.response

                if resp:
                    deps[dep] = {
                        'code': resp.code,
                        'error': resp.body.decode()
                    }
                else:
                    deps[dep] = {
                        'error': str(http_err)
                    }
            except Exception as err:

                log.error(
                    "Dependent service '{}' connection error @ '{}': {}"
                    "".format(dep, url, err))

                deps[dep] = {'error': str(err)}
            else:
                deps[dep] = json_decode(resp.body)

        raise gen.Return(deps)
