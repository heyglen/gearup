# -*- coding: utf-8 -*-

import logging

from invoke import task

from gearup.commands.pip import Pip


logger = logging.getLogger(__name__)


@task()
def download(ctx, download_path, package):
    return Pip.download(ctx, download_path, package)


@task()
def install(ctx, package):
    return Pip.download(ctx, package)
