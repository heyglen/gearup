# -*- coding: utf-8 -*-

import os
import logging

from invoke import task

from gearup.commands.http import Http
from gearup.commands.file_system import FileSystem
from gearup.commands.packages import Packages


logger = logging.getLogger(__name__)


@task
def install(ctx, package):
    return Packages.install(ctx, package)
