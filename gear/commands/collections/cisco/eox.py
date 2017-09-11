import logging

import click
from invoke import task

from gear.commands.cisco.eox.eox import Eox


logger = logging.getLogger(__name__)


@task(default=True)
def list(ctx):
    cisco_eox = Eox()
    for eox in cisco_eox.list():
        click.echo(eox)
    # console = BaseCiscoApiConsole()

@task()
def by_product(ctx, product):
    cisco_eox = Eox()
    for eox in cisco_eox.by_product(product):
        click.echo(eox)
    # console = BaseCiscoApiConsole()