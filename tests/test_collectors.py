# -*- coding: utf-8 -*-
"""Collectors tests."""
import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from datetime import datetime

import six
from tornadoappinfo import collectors

if six.PY2:
    import time

    def to_timestamp(dt):
        return time.mktime(dt.timetuple())
else:
    def to_timestamp(dt):
        return dt.timestamp()


class CollectorsTestCase(unittest.TestCase):

    @mock.patch("tornadoappinfo.collectors.datetime")
    def test_app_load_time(self, mck_datetime):
        mck_datetime.datetime.now.return_value = datetime(2014, 1, 1, 1, 1, 1)

        value = collectors.app_load_time()
        self.assertEqual(value, "2014-01-01T01:01:01")

    @mock.patch("tornadoappinfo.collectors._head_info")
    @mock.patch("tornadoappinfo.collectors._current_branch")
    def test_git_state(self, current_branch, head_info):
        current_branch.return_value = "master"
        head_info.return_value = (
            "abcd1234def",
            "Kamilek",
            "message",
            int(to_timestamp(datetime(2014, 2, 2, 2, 2, 2))))

        result = collectors.git_state()

        self.assertEqual(result['rev'], "abcd1234def")
        self.assertEqual(result['date'], "2014-02-02T02:02:02")
        self.assertEqual(result['message'], "message")
        self.assertEqual(result['author'], "Kamilek")
        self.assertEqual(result['branch'], "master")

    @mock.patch("tornadoappinfo.collectors.subprocess")
    def test__git(self, subprocess):
        subprocess.check_output.return_value = "test"
        self.assertEqual(collectors._git(), "test")

        subprocess.check_output.return_value = six.u("ótest")
        self.assertEqual(collectors._git(), six.u("ótest"))
