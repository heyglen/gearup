# -*- coding: utf-8 -*-

import logging

from invoke import task

from gear.versions import Version
from gear.commands.git import Git
from gear.collections.git_flow import git_flow_release_start, git_flow_release_finish

logger = logging.getLogger(__name__)


@task(default=True)
def current(ctx):
    current = Version.current()
    logger.info(current)
    return current


@task
def major(ctx, deploy=False):
    return version_bump(ctx, 'major', Version.major(), deploy=deploy)


@task
def minor(ctx, deploy=False):
    return version_bump(ctx, 'minor', Version.minor(), deploy=deploy)


@task
def patch(ctx, deploy=False):
    return version_bump(ctx, 'patch', Version.patch(), deploy=deploy)


def version_bump(ctx, version_bump_type, version, deploy):
    if Git.is_dirty(ctx):
        logger.debug('Version bump skipped, working directory is clean')
        return Version.current()
    Version.validate(version)
    Version.validate_update(version)
    logger.debug('Bump {} version'.format(version_bump_type))
    Git.add(ctx, '*.py')
    Git.commit(ctx)
    version = getattr(Version, version_bump_type)()
    git_flow_release_start(ctx, version)
    ctx.run('bumpversion {}'.format(version_bump_type))
    Git.commit(ctx, 'Version bump to {}'.format(version))
    git_flow_release_finish(ctx, version)
    return Version.current()
