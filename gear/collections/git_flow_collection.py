# -*- coding: utf-8 -*-

import logging

from invoke import task, Collection


logger = logging.getLogger(__name__)


@task(name='start')
def git_flow_release_start(ctx, version):
    command = 'git flow release start {}'.format(version)
    logger.debug(command)
    ctx.run(command)


@task(name='finish')
def git_flow_release_finish(ctx, version):
    command = 'git flow release finish {0} -m {0}'.format(version)
    logger.debug(command)
    ctx.run(command)


ns_git_flow = Collection(
    Collection(
        'release',
        git_flow_release_start,
        git_flow_release_finish,
    )
)
