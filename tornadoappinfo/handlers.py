"""App Info handler."""
from tornado.web import RequestHandler
from tornado.escape import json_encode
from tornado import gen


class InfoHandler(RequestHandler):

    def get(self):
        self.write(json_encode(self.application.info))
        self.finish()
