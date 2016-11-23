# -*- coding: utf-8 -*-

import logging
from datetime import datetime


logger = logging.getLogger(__name__)


class Git(object):

    @classmethod
    def add(cls, cli, files):
        if isinstance(files, basestring):
            files = [files]
        items = ' '.join(files)
        command = 'git add {}'.format(items)
        command = command.replace('  ', ' ').strip()
        logger.debug(command)
        cli.run(command)

    @classmethod
    def status(cls, cli, message=None, everything=True):
        command = '{} status'.format('git')
        logger.debug(command)
        cli.run(command)

    @classmethod
    def commit(cls, cli, message=None, everything=True):
        if not message:
            message = datetime.now().strftime('%d-%m-%Y %H:%M:%M')
            logger.debug('Using default commit message {}'.format(message))
        add_all_flag = ''
        if everything:
            add_all_flag = '-a '
        command = 'git commit {}-m "{}"'.format(add_all_flag, message)
        logger.debug(command)
        cli.run(command)

    @classmethod
    def push(cls, cli, remote='origin', branch='master'):
        command = 'git push {} {}'.format(remote, branch)
        logger.debug(command)
        cli.run(command)

    @classmethod
    def is_dirty(cls, cli):
        is_dirty = True
        command = 'git diff'
        logger.debug(command)
        output = cli.run(command)
        if output.stderr.strip():
            logger.error(output.stderr)
            raise ValueError(output.stderr)
        if output.stdout.strip():
            logger.debug('Dirty')
        else:
            is_dirty = False
            logger.debug('Clean')
        return is_dirty
