# -*- coding: utf-8 -*-


import os
import logging


from gearup.commands.file_system import FileSystem


logger = logging.getLogger(__name__)


class Pip(object):

    @classmethod
    def verify_package(cls, package):
        if ' ' in package:
            raise ValueError('Invalid package {}. Pip packages must not contain spaces.'.format(
                package
            ))

    @classmethod
    def download(cls, cli, download_path, package, source=False):
        cls.verify_package(package)
        if download_path is None:
            download_path = os.getcwd()
        else:
            download_path = FileSystem.get_directory(download_path)
        source_command = ''
        if source:
            source_command = ' --no-binary :all: '

        command = 'pip download {}  -d {} {}'.format(
            source_command,
            download_path,
            package,
        ).replace('  ', ' ').strip()
        logger.debug(command)
        cli.run(command)

    @classmethod
    def install(cls, cli, package):
        cls.verify_package(package)
        command = 'pip install {}'.format(
            package,
        ).replace('  ', ' ').strip()
        logger.debug(command)
        cli.run(command)

    @classmethod
    def upgrade(cls, cli, package):
        cls.verify_package(package)
        command = 'pip install -U {}'.format(
            package,
        ).replace('  ', ' ').strip()
        logger.debug(command)
        cli.run(command)
