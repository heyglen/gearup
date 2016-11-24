# -*- coding: utf-8 -*-

import logging

import click
from invoke import task

from gearup.commands.cisco.psirt import Psirt


logger = logging.getLogger(__name__)


@task
def advisories(ctx, year=None):
    for advisory in Psirt().get_advisories(year):
        click.echo(advisory)
