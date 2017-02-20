# -*- coding: utf-8 -*-

import os
import logging
import shutil


from gear.commands.operating_system import OperatingSystem


logger = logging.getLogger(__name__)


class FileSystem(object):

    @classmethod
    def executable(cls, ctx, file_name, group='u', raise_exception=True):
        return cls._file_chomod(
            ctx,
            file_name,
            permission='x',
            group=group,
            raise_exception=raise_exception,
        )

    @classmethod
    def _file_chomod(cls, ctx, file_name, permission, group='u', raise_exception=True):
        operating_system = OperatingSystem.name()
        if operating_system == 'windows':
            message = 'Skipping credentials modification on unsupported platform {}'.format(
                operating_system
            )
            logger.error(message)
            # if raise_exception:
            #     raise SystemError(message)
        else:
            return cls._linux_set_permission(ctx, file_name, permission, group)

    @classmethod
    def _linux_set_permission(cls, ctx, file_name, permission, group='u'):
        if permission not in ['r', 'w', 'x']:
            raise ValueError('Invalid permission "{}"'.format(permission))
        if group not in ['u', 'g', 'o']:
            raise ValueError('Invalid permission "{}"'.format(group))
        command = 'chmod {}+{} {}'.format(group, permission, file_name)
        logger.debug(command)
        return ctx.run(command)

    @classmethod
    def get_directory(cls, path):
        if path in ('.', '..'):
            path = os.path.abspath(path)
        else:
            if not path.endswith(os.path.sep):
                directories = path.split(os.path.sep)[:-1]
                path = os.path.sep.join(directories)
            cls.is_directory(path)
        return path

    @classmethod
    def is_directory(cls, directory, raise_exception=True):
        if not os.path.isdir(directory):
            if raise_exception:
                raise ValueError('{}: Invalid Directory'.format(directory))
            return False
        return True

    @classmethod
    def is_file(cls, file_name, raise_exception=True):
        if not os.path.isfile(file_name):
            if raise_exception:
                raise ValueError('{}: Invalid File'.format(file_name))
            return False
        return True

    @classmethod
    def copy(cls, source, destination):
        cls.is_file(source, raise_exception=True)
        if not (cls.is_file(destination, raise_exception=False) or
                cls.is_file(destination, raise_exception=False)):
            message = 'Destination {} must be a file or directory'.format(destination)
            logger.error(message)
            raise ValueError(message)
        shutil.copyfile(source, destination)

    @classmethod
    def get_file(cls, file_path):
        file_path = os.path.abspath(file_path)
        if not os.path.isfile(file_path):
            raise ValueError('{}: Invalid File'.format(file_path))
        logger.debug('Get file {}'.format(file_path))
        return file_path
