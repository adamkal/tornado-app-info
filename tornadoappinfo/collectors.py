"""Collectors."""

import subprocess
import datetime


def app_load_time():
    """Gets moment at which the app was loaded to memory.

    :return: datetime in iso format.

    """
    return datetime.datetime.now().isoformat()


def git_state():
    """Gets information about git repository state."""
    rev, author, msg, timestamp = _head_info()
    branch = _current_branch()
    timestamp = int(timestamp)
    to_datetime = datetime.datetime.fromtimestamp

    return {
        'rev': rev,
        'date': to_datetime(timestamp).isoformat(),
        'message': msg,
        'author': author,
        'branch': branch
    }


def _git(*args):
    return subprocess.check_output(['git'] + list(args))


def _head_info():
    return _git('log', '--pretty=format:%H;%an;%s;%ct', '-1').decode().split(';')


def _current_branch():
    branches = _git('branch').decode().split()
    return branches[branches.index('*') + 1]
