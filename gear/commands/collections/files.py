# -*- coding: utf-8 -*-

import logging

from invoke import task

from gear.commands.watch_dog import WatchDog
from gear.commands.file_system import FileSystem
from gear.commands.operating_system import OperatingSystem


logger = logging.getLogger(__name__)


@task(name='execute')
def execute_command(ctx, command, sudo=True):
    return OperatingSystem.execute(ctx, command, sudo=sudo)


@task(name='executable')
def set_executable(ctx, file_name, group='u', raise_exception=True):
    return FileSystem.executable(ctx, file_name, group='u', raise_exception=True)


@task(name='sync')
def sync(ctx, source, destination):
    return WatchDog.modified(source, FileSystem.copy, source=source, destination=destination)
