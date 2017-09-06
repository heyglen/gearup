
import logging
import pathlib

import click
import yaml

from gear.utils.configuration import (configuration_directory,
                                      configuration_path,
                                      default_configuration)
from invoke import task

logger = logging.getLogger(__name__)

@task(name='edit', default=True)
def edit(ctx):
    if not configuration_path.is_file():
        if not configuration_directory.is_dir():
            configuration_directory.mkdir(parents=True)
        configuration_path.touch()
        text = yaml.dump(default_configuration, default_flow_style=False)
        configuration_path.write_text(text)
        logger.debug(f'Configuration file created in {configuration_path}')
    click.edit(filename=str(configuration_path))
