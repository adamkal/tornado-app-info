"""Collectors."""

import datetime


def app_load_time():
    """Gets moment at which the app was loaded to memory.

    :return: datetime in iso format.

    """
    return datetime.datetime.now().isoformat()
