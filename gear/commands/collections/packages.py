# -*- coding: utf-8 -*-

import os
import logging

from invoke import task

from gear.commands.http import Http
from gear.commands.file_system import FileSystem
from gear.commands.packages import Packages


logger = logging.getLogger(__name__)


@task
def install(ctx, package):
    return Packages.install(ctx, package)
