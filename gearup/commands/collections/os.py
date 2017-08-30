# -*- coding: utf-8 -*-

import logging

from invoke import task

from gearup.commands.operating_system import OperatingSystem


logger = logging.getLogger(__name__)



@task(name='name')
def get_os_name(ctx):
    return OperatingSystem.name()

