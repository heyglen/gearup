# -*- coding: utf-8 -*-

import sys
import logging


logger = logging.getLogger(__name__)


class OperatingSystem(object):

    @classmethod
    def name(cls):
        logger.debug('Get platform')
        os_name = 'unknown'
        if sys.platform == 'win32':
            os_name = 'windows'
        return os_name

    @classmethod
    def execute(cls, ctx, command, sudo=True):
        operating_system = cls.name()
        command = command.strip()
        if operating_system != 'windows' and sudo and not command.startswith('sudo '):
            command = 'sudo {}'.format(command)
        logger.debug(command)
        return ctx.run(command)
