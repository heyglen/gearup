# -*- coding: utf-8 -*-

import logging

from invoke import task

from gearup.commands.collections import git_flow


logger = logging.getLogger(__name__)


@task(name='update', default=True)
def update(ctx):
    logger.debug('Updating software')
    logger.debug('Updating git flow')
    git_flow.install_git_flow(ctx)
