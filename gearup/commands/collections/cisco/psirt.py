# -*- coding: utf-8 -*-

import logging

import click
from invoke import task

from gearup.commands.cisco.psirt import Psirt


logger = logging.getLogger(__name__)


@task
def issues(ctx, year=None, critical=None, high=None, medium=None, low=None):
    for advisory in Psirt().issues(year=year, critical=critical, high=high, medium=medium, low=low):
        click.echo(advisory)


@task
def get(ctx, identifier):
    click.echo(Psirt().get(identifier))
