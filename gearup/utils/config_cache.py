# -*- coding: utf-8 -*-

import operator
import datetime
import logging

from invoke.config import Config

logger = logging.getLogger(__name__)


class Cache(object):
    pass


class ConfigCache(object):
    _cache_key_name = 'cache'

    def __init__(self, app):
        config = Config()
        try:
            cache = getattr(operator.attrgetter(app)(config), self._cache_key_name)
        except AttributeError:
            cache = Cache()
        self.cache = cache

    def _get_or_create(self, current, key):
        try:
            value = getattr(current, key)
        except AttributeError:
            setattr(current, key, dict())
        return value

    def set(self, key, value, timeout):
        setattr(self.cache, key, value)
        setattr(self.cache, '{}_timeout'.format(key), timeout)

    def get(self, key):
        try:
            timeout = getattr(self.cache, '{}_timeout'.format(key))
        except AttributeError:
            return None
        now = datetime.datetime.now()
        timeout = now + datetime.timedelta(seconds=timeout)
        if now < timeout:
            logger.debug('Cache timeout')
            self.delete(key)
        else:
            return getattr(self.cache, key)

    def delete(self, key):
        delattr(self.cache, key)
        delattr(self.cache, '{}_timeout'.format(key))
