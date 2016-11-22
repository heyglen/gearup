# -*- coding: utf-8 -*-

import re
import sys
import logging


logger = logging.getLogger(__name__)

from gearup.commands.operating_system import OperatingSystem


class Packages(object):
    _apt_package_re = re.compile(r'apt install (?P<package>\S+)')
    _apt_package_not_found = 'unable to locate package'

    @classmethod
    def _apt_guess_package(cls, cli, package):
        logger.debug('Guessing package name by running \'{}\' as executable'.format(package))
        output = cli.run(package)
        match = cls._apt_package_re.search(output)
        if match:
            package_name = match.group('package')
            logger.debug('Found package name \'{}\''.format(package_name))
            return package_name


    @classmethod
    def _apt_install(cls, cli, package):
        if not cls._do_apt_install(cli, package):
            guessed_package = cls._apt_guess_package(cli, package)
            if not cls._do_apt_install(cli, guessed_package):
                message = 'Package {} not found'.format(package)
                logger.error(message)
                raise SystemError(message)
        return True

    @classmethod
    def _do_apt_install(cls, cli, package):
        output = cli.run('sudo apt install {}'.format(package))
        if cls._apt_package_not_found in output.stdout:
            logger.debug('Package {} not found'.format(package))
            return False
        return True            

    @classmethod
    def install(cls, cli, package):
        os_name = OperatingSystem.name()
        if os_name == 'ubuntu':
            response = cls._apt_install(cli, package)
        else:
            raise NotImplemented('Installation on OS {} not implemented'.format(os_name))
        return response