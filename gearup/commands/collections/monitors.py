# -*- coding: utf-8 -*-

import os
import logging

from invoke import task

from gearup.commands.http import Http
from gearup.commands.file_system import FileSystem
from gearup.commands.uptimerobot import UpTimeRobot


logger = logging.getLogger(__name__)


@task(name='list', default=True)
def graphs(ctx):
    return UpTimeRobot.monitors(ctx)


@task(name='get')
def graph(ctx, friendly_name):
    return UpTimeRobot.graph(friendly_name, ctx)
