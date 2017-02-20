# -*- coding: utf-8 -*-

import logging

from invoke import task

logger = logging.getLogger(__name__)


@task(name='ssh')
def ssh(ctx, hostname, command=''):
    extra_command = ''
    if command:
        extra_command = ' "{}"'.format(command.strip('"'))
    command = 'ssh {}{}'.format(hostname, extra_command)
    logger.debug(command)
    ctx.run(command)
