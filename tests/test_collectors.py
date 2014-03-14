"""Collectors tests."""
import unittest
import unittest.mock
from datetime import datetime

from tornadoappinfo import collectors


class CollectorsTestCase(unittest.TestCase):

    @unittest.mock.patch("tornadoappinfo.collectors.datetime")
    def test_app_load_time(self, mck_datetime):
        mck_datetime.datetime.now.return_value = datetime(2014, 1, 1, 1, 1, 1)

        value = collectors.app_load_time()
        self.assertEqual(value, "2014-01-01T01:01:01")

    @unittest.mock.patch("tornadoappinfo.collectors._head_info")
    @unittest.mock.patch("tornadoappinfo.collectors._current_branch")
    def test_git_state(self, current_branch, head_info):
        current_branch.return_value = "master"
        head_info.return_value = (
            "abcd1234def",
            "Kamilek",
            "message",
            int(datetime(2014, 2, 2, 2, 2, 2).timestamp()))

        result = collectors.git_state()

        self.assertEqual(result['rev'], "abcd1234def")
        self.assertEqual(result['date'], "2014-02-02T02:02:02")
        self.assertEqual(result['message'], "message")
        self.assertEqual(result['author'], "Kamilek")
        self.assertEqual(result['branch'], "master")
