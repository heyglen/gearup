# -*- coding: utf-8 -*-

import logging

import click
from invoke import task

from gear.commands.cisco.psirt import Psirt


logger = logging.getLogger(__name__)


@task(default=True)
def list(ctx, critical=True, high=True, medium=None, low=None):
    for advisory in Psirt().list(critical=critical, high=high, medium=medium, low=low):
        click.echo(advisory)


@task
def get(ctx, identifier):
    click.echo(Psirt().get(identifier))
