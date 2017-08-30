# -*- coding: utf-8 -*-

import logging

from invoke import task

from gear.commands.pip import Pip


logger = logging.getLogger(__name__)


@task()
def download(ctx, package, download_path=None, source=False):
    return Pip.download(ctx, package, download_path=download_path, source=source)


@task()
def install(ctx, package):
    return Pip.download(ctx, package)
