# -*- coding: utf-8 -*-

import logging

from invoke import task

logger = logging.getLogger(__name__)


@task(name='scp')
def scp(ctx, source, destination):
    command = 'scp {} {}'.format(source, destination)
    logger.debug(command)
    ctx.run(command)
