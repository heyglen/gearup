# -*- coding: utf-8 -*-

import logging

from invoke import task, Collection

from gearup.utils.file_system import FileSystem
from gearup.utils.operating_system import OperatingSystem


logger = logging.getLogger(__name__)


@task(name='execute')
def execute_command(ctx, command, sudo=True):
    return OperatingSystem.execute(ctx, command, sudo=sudo)


@task(name='executable')
def set_executable(ctx, file_name, group='u', raise_exception=True):
    return FileSystem.executable(ctx, file_name, group='u', raise_exception=True)


