# -*- coding: utf-8 -*-

import logging

from invoke import task, Collection

from gearup.collections import git_flow_collection
from gearup.collections.http_collection import http_download


logger = logging.getLogger(__name__)


@task(name='update', default=True)
def update(ctx):
    logger.debug('Updating software')
    logger.debug('Updating git flow')
    git_flow_collection.install_git_flow(ctx)


