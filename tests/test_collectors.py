"""Collectors tests."""
import os
import unittest
import unittest.mock
from datetime import datetime

from tornadoappinfo import collectors

this_file = os.path.dirname(__file__)
PROJECT_PATH = os.path.join(this_file, os.path.pardir)
del this_file


class CollectorsTestCase(unittest.TestCase):

    @unittest.mock.patch("tornadoappinfo.collectors.datetime")
    def test_app_load_time(self, mck_datetime):
        mck_datetime.datetime.now.return_value = datetime(2014, 1, 1, 1, 1, 1)

        value = collectors.app_load_time()
        self.assertEqual(value, "2014-01-01T01:01:01")

    @unittest.mock.patch("tornadoappinfo.collectors.Repository")
    def test_git_state(self, Repository):
        repo = Repository.return_value
        repo.head.shorthand = "master"
        obj = repo.head.get_object.return_value
        obj.hex = "abcd1234def"
        obj.commit_time = int(datetime(2014, 2, 2, 2, 2, 2).timestamp())
        obj.message = "message"
        obj.committer.name = "Kamilek"

        git_state = collectors.git_state(PROJECT_PATH)
        result = git_state()

        self.assertEqual(result['rev'], "abcd1234def")
        self.assertEqual(result['date'], "2014-02-02T02:02:02")
        self.assertEqual(result['message'], "message")
        self.assertEqual(result['author'], "Kamilek")
        self.assertEqual(result['branch'], "master")
