# -*- coding: utf-8 -*-

import sys
import logging


from gearup.utils.operating_system import OperatingSystem


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
	        message = 'Unsupported platform {}'.format(operating_system)
	        logger.error('Unsupported platform {}'.format(operating_system))
	        if raise_exception:
	            raise SystemError(message)
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
	    

