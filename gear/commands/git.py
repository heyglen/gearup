# -*- coding: utf-8 -*-

import logging
from datetime import datetime


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
    def add(cls, cli, files=None):
        files = files or '*'
        if isinstance(files, str):
            files = [files]
        items = ' '.join(files)
        command = 'git add {}'.format(items)
        command = command.replace('  ', ' ').strip()
        logger.debug(command)
        return cli.run(command)

    @classmethod
    def status(cls, cli, message=None, everything=True):
        command = '{} status'.format('git')
        logger.debug(command)
        return cli.run(command, hide=True)

    @classmethod
    def commit(cls, cli, message=None, everything=True):
        result = None
        status = cls.status(cli, message=message, everything=everything)
        if 'nothing to commit, working directory clean' in status.stdout:
            logger.info('Commit skipped: working directory clean.')
        else:
            if not message:
                message = datetime.now().strftime('%d-%m-%Y %H:%M:%M')
                logger.debug('Using default commit message {}'.format(message))
            add_all_flag = ''
            if everything:
                add_all_flag = '-a '
            command = 'git commit {}-m "{}"'.format(add_all_flag, message)
            logger.debug(command)
            result = cli.run(command)
            if 'no changes added to commit' in result.stderr:
                raise GitCommitError(result.stderr)
        return result

    @classmethod
    def push(cls, cli, remote='origin', branch=None, force=False):
        if branch is None:
            branches = cls.remote(cli)
        elif isinstance(branch, str):
            branches = [branch]
        branches = ' '.join(branches)
        response = cls.checkout(cli, branch=branch)
        result = None
        if cls._success('push', response) or force:
            command = 'git push {} {}'.format(remote, branches)
            logger.debug(command)
            result = cli.run(command)
        else:
            logger.info('Push skipped: remote directory up to date.')
        return result

    @classmethod
    def _success(cls, action, response):
        for stream, messages in cls._success_messages[action].items():
            for message in messages:
                if message in getattr(response, stream):
                    return True
        return False

    @classmethod
    def checkout(cls, cli, branch='master'):
        command = 'git checkout {}'.format(branch)
        logger.debug(command)
        response = cli.run(command, hide=True)
        if not cls._success('checkout', response):
            raise GitCheckoutError('{}\n\n{}'.format(response.stdout, response.stderr))
        return response

    @classmethod
    def remote(cls, cli):
        command = 'git remote'
        logger.debug(command)
        response = cli.run(command, hide=True)
        return response.stdout.splitlines()

    @classmethod
    def is_dirty(cls, cli):
        is_dirty = True
        command = 'git diff'
        logger.debug(command)
        output = cli.run(command)
        if output.stderr.strip():
            logger.error(output.stderr)
            raise ValueError(output.stderr)
        if not output.stdout.strip():
            is_dirty = False
        return is_dirty
