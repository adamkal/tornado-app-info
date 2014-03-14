#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_tornadoappinfo
----------------------------------

Tests for `tornadoappinfo` module.
"""

import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from tornado.web import Application as TornadoApplication
from tornadoappinfo import application


class TestApp(application.VersionMixin, TornadoApplication):

    info_collectors = {
        'version': mock.MagicMock()
    }


class VersionMixinTestCase(unittest.TestCase):

    def test_collect_info(self):
        Application = TestApp

        Application.info_collectors['version'].side_effect = ["v1", "v2"]

        app = Application()

        # this should return the version loaded to memory so it's the current
        # code at beginning
        assert app.info['version'] == "v1"
        Application.info_collectors['version'].assert_called_once_with()

        # .. but the current code versioL might change after application was
        # loaded so the function might change it's value
        assert app.info_collectors['version']() == "v2"


if __name__ == '__main__':
    unittest.main()
