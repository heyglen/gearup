import logging

from invoke import task

from gear.commands.cisco.eox.eox import BaseCiscoApiConsole


logger = logging.getLogger(__name__)


@task(default=True)
def list(ctx):
    console = BaseCiscoApiConsole()