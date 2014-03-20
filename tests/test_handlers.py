"""Test App Info handler."""
try:
    from unittest import mock
except ImportError:
    import mock

from tornado.testing import AsyncHTTPTestCase
from tornado.escape import json_decode, json_encode
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
        self.write(json_encode({'version': 1}))


class InfoHandlerTestCase(AsyncHTTPTestCase):

    def setUp(self):
        TestApp.info_collectors['version'].side_effect = ("v1", "v2")
        TestApp.info_collectors['deploy_time'].side_effect = ("11.11.2011",
                                                              "12.12.2012")
        super(InfoHandlerTestCase, self).setUp()

        TestApp.info_dependencies = {
            'external_dep': self._ext_url
        }

    @property
    def _ext_url(self):
        return self.get_url('/fake_external_info')

    def get_app(self):
        return TestApp([
            ('/info', InfoHandler),
            ('/fake_external_info', FakeExternalInfoHandler),
        ])

    def assertStartsWith(self, string, prefix):
        starts_with = string.startswith(prefix)
        self.assertTrue(starts_with,
                        "'{}' does not start with '{}'".format(string, prefix))

    def test_get_info(self):
        self.http_client.fetch(self.get_url('/info'), self.stop)
        response = self.wait()

        self.assertEqual(response.code, 200)
        data = json_decode(response.body)

        self.assertEqual(data['version'], "v1")
        self.assertEqual(data['deploy_time'], "11.11.2011")

        external_dep = data['dependencies']['external_dep']
        self.assertEqual(external_dep['version'], 1)
        self.assertEqual(external_dep['url'], self._ext_url)

    @mock.patch('tornadoappinfo.handlers.log')
    def test_get_info_dep_404(self, log):
        invalid_url = self.get_url('/invalid_url')
        TestApp.info_dependencies['404'] = invalid_url
        info_url = self.get_url('/info')

        self.http_client.fetch(info_url, self.stop)
        response = self.wait()

        self.assertEqual(response.code, 200)
        data = json_decode(response.body)

        dependencies = data['dependencies']
        self.assertEqual(dependencies['external_dep']['version'], 1)
        self.assertEqual(dependencies['external_dep']['url'], self._ext_url)
        self.assertEqual(dependencies['404']['code'], 404)
        self.assertEqual(dependencies['404']['url'], invalid_url)

        args, kwargs = log.error.call_args
        self.assertStartsWith(
            args[0],
            "Dependent service '404' error @ '{}':".format(invalid_url))

        del TestApp.info_dependencies['404']

    @mock.patch('tornadoappinfo.handlers.log')
    def test_get_info_dep_wrong_url(self, log):
        info_deps = TestApp.info_dependencies
        wrong_url = info_deps['wrong_url'] = "http://thisdoesnotexist.wrong"
        info_url = self.get_url('/info')

        self.http_client.fetch(info_url, self.stop)
        response = self.wait()

        self.assertEqual(response.code, 200)
        data = json_decode(response.body)

        dependencies = data['dependencies']
        self.assertEqual(dependencies['external_dep']['version'], 1)
        self.assertEqual(dependencies['external_dep']['url'], self._ext_url)
        self.assertTrue(len(dependencies['wrong_url']['error']))
        self.assertEqual(dependencies['wrong_url']['url'], wrong_url)

        args, kwargs = log.error.call_args
        self.assertStartsWith(
            args[0],
            "Dependent service 'wrong_url' connection error @ '{}':"
            "".format(wrong_url))

        del TestApp.info_dependencies['wrong_url']
