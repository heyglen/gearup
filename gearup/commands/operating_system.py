# -*- coding: utf-8 -*-

import sys
import logging
import platform


logger = logging.getLogger(__name__)


class OperatingSystem(object):
    _os_name = None

    @classmethod
    def name(cls):
        logger.debug('Get OS name')
        if cls._os_name is None:
            os_name = 'unknown'
            if sys.platform == 'win32':
                os_name = 'windows'
            else:
                os_name = platform.linux_distribution()[0].lower()
            cls._os_name = os_name
        logger.debug('OS is {}'.format(cls._os_name))
        return cls._os_name

    @classmethod
    def execute(cls, ctx, command, sudo=True):
        operating_system = cls.name()
        command = command.strip()
        if operating_system != 'windows' and sudo and not command.startswith('sudo '):
            command = 'sudo {}'.format(command)
        logger.debug(command)
        return ctx.run(command)
