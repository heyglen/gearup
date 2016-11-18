# -*- coding: utf-8 -*-

import os
import re
import logging
import ConfigParser

logger = logging.getLogger(__name__)


class Version(object):
    valid_version = re.compile(r'^\d+\.\d+\.\d+$')

    @classmethod
    def current(cls):
        version = 'unknown'
        setup_file = 'setup.cfg'
        if os.path.isfile(setup_file):
            logger.debug('Returning version from {}'.format(os.path.abspath(setup_file)))
            config = ConfigParser.RawConfigParser()
            config.read(setup_file)
            version = config.get('bumpversion', 'current_version')
        else:
            logger.debug("Returning {}'s version".format(__name__))

        return version

    @classmethod
    def patch(cls):
        current = cls.current()
        cls.validate(current)
        (major, minor, patch) = current.split('.')
        patch = str(int(patch) + 1)
        return '.'.join([major, minor, patch])

    @classmethod
    def minor(cls):
        current = cls.current()
        cls.validate(current)
        (major, minor, patch) = current.split('.')
        minor = str(int(minor) + 1)
        return '.'.join([major, minor, patch])

    @classmethod
    def major(cls):
        current = cls.current()
        cls.validate(current)
        (major, minor, patch) = current.split('.')
        major = str(int(major) + 1)
        return '.'.join([major, minor, patch])

    @classmethod
    def validate_update(cls, version, raise_exception=True):
        valid = False
        current_version = cls.current()
        if current_version == version:
            raise ValueError('Specified version {} matches current version'.format(version))
        (major, minor, patch) = current_version.split('.')
        (new_major, new_minor, new_patch) = version.split('.')
        (major, minor, patch) = (int(major), int(minor), int(patch))
        (new_major, new_minor, new_patch) = (int(new_major), int(new_minor), int(new_patch))
        for current, new in zip([major, minor, patch], [new_major, new_minor, new_patch]):
            if new > current:
                valid = True
                break
        else:
            if raise_exception:
                raise ValueError('New version {} is older then current version {}'.format(
                    version,
                    current_version
                ))
        return valid

    @classmethod
    def validate(cls, version, raise_exception=True):
        valid = False
        if cls.valid_version.match(version):
            valid = True
        elif raise_exception:
            raise ValueError('Invalid version "{}"'.format(version))
        return valid
