import logging
import os
import time

import git


CACHE_TTL = 300
REPO_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.cloned-repository')
REPO_URL = os.getenv('REPO_URL', 'https://github.com/dbazile/bazile.org')

_time_of_last_pull = -1


def pull():
    global _time_of_last_pull
    log = logging.getLogger(__name__)
    if not os.path.isdir(REPO_PATH):
        log.info('Cloning repository from %s', REPO_URL)
        git.Repo.clone_from(REPO_URL, REPO_PATH)
    else:
        log.info('Updating from %s', REPO_URL)
        git.Repo(REPO_PATH).remote().pull()
    log.info('Done; HEAD is now commit %s', get_commit())
    _time_of_last_pull = time.time()


def pull_if_needed():
    log = logging.getLogger(__name__)
    seconds_remaining = time.time() - _time_of_last_pull
    if CACHE_TTL > seconds_remaining:
        log.info('Cache is still valid for another %d seconds', CACHE_TTL - seconds_remaining)
        return
    pull()


def get_commit() -> str:
    return str(git.Repo(REPO_PATH).head.commit)
