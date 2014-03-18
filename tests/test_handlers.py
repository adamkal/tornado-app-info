"""Test App Info handler."""
import json

try:
    from unittest import mock
except ImportError:
    import mock

from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application, RequestHandler

from tornadoappinfo.application import VersionMixin
from tornadoappinfo.handlers import InfoHandler


class TestApp(VersionMixin, Application):

    info_collectors = {
        'version': mock.MagicMock(),
        'deploy_time': mock.MagicMock()
    }


class FakeExternalInfoHandler(RequestHandler):

    def get(self):
        self.write(json.dumps({'version': 1}))


class InfoHandlerTestCase(AsyncHTTPTestCase):

    def setUp(self):
        TestApp.info_collectors['version'].side_effect = ("v1", "v2")
        TestApp.info_collectors['deploy_time'].side_effect = ("11.11.2011",
                                                              "12.12.2012")
        super(InfoHandlerTestCase, self).setUp()

        TestApp.info_dependencies = {
            'external_dep': self.get_url('/fake_external_info')
        }

    def get_app(self):
        return TestApp([
            ('/info', InfoHandler),
            ('/fake_external_info', FakeExternalInfoHandler),
        ])

    def test_get_info(self):
        self.http_client.fetch(self.get_url('/info'), self.stop)
        response = self.wait()

        data = json.loads(response.body.decode())

        self.assertEqual(data['version'], "v1")
        self.assertEqual(data['deploy_time'], "11.11.2011")
        self.assertEqual(data['dependencies']['external_dep'], {'version': 1})
