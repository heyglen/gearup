# -*- coding: utf-8 -*-

import os
import sys
import logging

from invoke import task, Collection

from gearup.collections import file_collection
from gearup.utils.operating_system import OperatingSystem
from gearup.collections.http_collection import http_download, get_url_filename


logger = logging.getLogger(__name__)

no_init_error = 'fatal: Not a gitflow-enabled repo yet. Please run "git flow init" first.'


@task(name='start')
def git_flow_release_start(ctx, version):
    command = 'git flow release start {}'.format(version)
    logger.debug(command)
    response = ctx.run(command)
    if no_init_error in response.stderr:
        raise ValueError('Uninitialized. Run: \'git flow init\'')

@task(name='finish')
def git_flow_release_finish(ctx, version):
    command = 'git flow release finish {0} -m {0}'.format(version)
    logger.debug(command)
    ctx.run(command)


@task(name='install')
def git_flow_install(ctx, raise_exception=True):
    operating_system_name = OperatingSystem.name()
    if operating_system_name == 'windows':
        message = 'Unsupported platform {}'.format(operating_system_name)
        logger.error(message)
        if raise_exception:
            raise SystemError(message)
    else:
        install_git_flow(ctx)


def install_git_flow(ctx):
    # https://github.com/nvie/gitflow/wiki/Linux#other-linuxes
    url = 'https://raw.github.com/nvie/gitflow/develop/contrib/gitflow-installer.sh'
    file_path = http_download(url)
    if not os.path.exists(file_path):
        raise ValueError('Unable to find file {}'.format(file_path))
    file_collection.set_executable(ctx, file_path)
    OperatingSystem.execute(ctx, file_path, sudo=True)
    os.remove(file_path)
    
