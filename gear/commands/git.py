import logging
from datetime import datetime

import git

logger = logging.getLogger(__name__)


class GitCheckoutError(Exception):
    pass


class GitCommitError(Exception):
    pass


class Git(object):
    _success_messages = {
        'push': {
            'stdout': [
                'Your branch is ahead of',
            ],
            'stderr': [
            ],
        },
        'checkout': {
            'stderr': [
                'Already on ',
            ],
            'stdout': [
                'Switched to branch',
            ],
        }
    }

    @classmethod
    def _get_repo(cls, directory=None):
        if directory is None:
            directory = str(pathlib.Path())
        return git.Repo(directory)


    @classmethod
    def add(cls, files=None):
        repo = cls._get_repo()
        if isinstance(files, list):
            repo.git.add(*files)
        else:
            repo.git.add(files)

    @classmethod
    def status(cls, message=None, everything=True):
        repo = cls._get_repo()
        return repo.git.status()

    @classmethod
    def commit(cls, message=None, everything=True):
        repo = cls._get_repo()
        result = None
        if everything:
            result = repo.git.commit('-am', message)
        else:
            result = repo.git.commit('-m', message)
        return result

    @classmethod
    def push(cls, remote='origin', branch=None):
        repo = cls._get_repo()
        if branch:
            result = repo.git.push(branch, remote)
        else:
            result = repo.git.push(branch, remote)
        return result

    @classmethod
    def checkout(cls, branch='master'):
        repo = cls._get_repo()
        return repo.git.checkout(branch)

    @classmethod
    def remote(cls):
        repo = cls._get_repo()
        return repo.git.remote()

    @classmethod
    def is_dirty(cls):
        raise NotImplemented('Not Implemented')
