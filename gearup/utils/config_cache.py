# -*- coding: utf-8 -*-

import datetime
import logging

from invoke.config import Config

logger = logging.getLogger(__name__)


class ConfigCache(object):
    _cache_key_name = 'cache'

    def __init__(self, app):
        self.app = Config()
        for step in app.split('.'):
            self.app = getattr(self.app, step)
        self.app = getattr(self.app, self._cache_key_name)

    def set(self, key, value, timeout):
        setattr(self.app, key, value)
        setattr(self.app, '{}_timeout'.format(key), timeout)

    def get(self, key):
        timeout = getattr(self.app, '{}_timeout'.format(key))
        now = datetime.datetime.now()
        timeout =  now + datetime.timedelta(seconds=timeout)
        if now < timeout:
            logger.debug('Cache timeout')
            self.delete(key)
        else:
            return getattr(self.app, key)

    def delete(self, key):
        delattr(self.app, key)
        delattr(self.app, '{}_timeout'.format(key))