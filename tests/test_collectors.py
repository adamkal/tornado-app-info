"""Collectors tests."""

from datetime import datetime

import unittest
import unittest.mock

from tornadoappinfo import collectors


class CollectorsTestCase(unittest.TestCase):

    @unittest.mock.patch("tornadoappinfo.collectors.datetime")
    def test_app_load_time(self, mck_datetime):
        mck_datetime.datetime.now.return_value = datetime(2014, 1, 1, 1, 1, 1)

        value = collectors.app_load_time()
        self.assertEqual(value, "2014-01-01T01:01:01")
