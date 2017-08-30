# -*- coding: utf-8 -*-

import logging

from invoke import task

from gear.commands.git import Git

logger = logging.getLogger(__name__)


@task(name='add')
def git_add(ctx, files):
    return Git.add(ctx, files)


@task(name='status')
def git_status(ctx, message=None, everything=True):
    return Git.status(ctx, message=message, everything=everything)


@task(name='commit')
def git_commit(ctx, message=None, everything=True):
    return Git.commit(ctx, message=message, everything=everything)


@task(name='push')
def git_push(ctx, remote='origin', branch='master'):
    return Git.push(ctx, remote=remote, branch=branch)


@task(name='dirty')
def is_dirty(ctx):
    return Git.is_dirty(ctx)
