"""Collectors."""

import datetime
from pygit2 import Repository


def app_load_time():
    """Gets moment at which the app was loaded to memory.

    :return: datetime in iso format.

    """
    return datetime.datetime.now().isoformat()


def git_state(repo_path):
    """Gets information about git repository state."""
    repo = Repository(repo_path)
    head = repo.head
    commit = head.get_object()
    to_datetime = datetime.datetime.fromtimestamp

    def _git_state():
        return {
            'rev': commit.hex,
            'date': to_datetime(commit.commit_time).isoformat(),
            'message': commit.message,
            'author': commit.committer.name,
            'branch': head.shorthand
        }

    return _git_state
