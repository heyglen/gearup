# -*- coding: utf-8 -*-

import logging
from datetime import datetime

from invoke import task

logger = logging.getLogger(__name__)


@task(name='add')
def git_add(ctx, files):
    if isinstance(files, basestring):
        files = [files]
    items = ' '.join(files)
    command = 'git add {}'.format(items)
    logger.debug(command)
    ctx.run(command)


@task(name='status')
def git_status(ctx, message=None, everything=True):
    command = '{} status'.format('git')
    logger.debug(command)
    ctx.run(command)


@task(name='commit')
def git_commit(ctx, message=None, everything=True):
    if not message:
        message = datetime.now().strftime('%d-%m-%Y %H:%M:%M')
        logger.debug('Using default commit message {}'.format(message))
    add_all_flag = ''
    if everything:
        add_all_flag = '-a '
    command = 'git commit {}-m "{}"'.format(add_all_flag, message)
    logger.debug(command)
    ctx.run(command)


@task(name='push')
def git_push(ctx, remote='origin', branch='master'):
    command = 'git push {} {}'.format(remote, branch)
    logger.debug(command)
    ctx.run(command)


@task(name='dirty')
def git_dirty(ctx):
    is_dirty = True
    command = 'git diff'
    logger.debug(command)
    output = ctx.run(command)
    if output.stderr.strip():
        logger.error(output.stderr)
        raise ValueError(output.stderr)
    if output.stdout.strip():
        logger.debug('Dirty')
    else:
        is_dirty = False
        logger.debug('Clean')
    return is_dirty
