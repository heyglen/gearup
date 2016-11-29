# -*- coding: utf-8 -*-

import inspect
from datetime import datetime
from datetime import timedelta
import logging
import operator
from functools import update_wrapper

from invoke.config import Config
from pymongo import MongoClient


logger = logging.getLogger(__name__)

config = Config()


class Cache(object):
    timestamp_attribute = 'cache_timestamp'
    cache_config_path = 'cache.document.db.mongodb'

    def __init__(self, fn):
        self.fn = fn
        self.module = self.get_method_module(self.fn)
        module_db = self.module.replace('.', '_')

        uri = self.get_configuration('cache.document.db.mongodb', 'uri')
        uri = uri or 'mongodb://localhost:27017'

        client = MongoClient(uri)
        self.database = client[module_db]
        logger.debug('Loaded cache db: {}'.format(module_db))

        timeout = self.get_configuration('cache.document.db', 'timeout')
        timeout = (timeout or 168) * -1  # In hours, one week default
        self.cache_expired = datetime.utcnow() - timedelta(hours=timeout)

    def get(self, *args, **kwargs):
        results = None
        cache = self.database[self.fn.func_name]
        search = {
            self.timestamp_attribute: {'$gt': self.cache_expired}
        }.update(kwargs)
        result_set = cache.find(search)
        result_count = result_set.count()
        if result_count:
            logger.debug('{}.{} returning {} cached results'.format(
                self.module,
                self.fn.func_name,
                result_count
            ))
            results = [r for r in result_set]
        return results

    def update(self, results):
        cache = self.database[self.fn.func_name]
        if isinstance(results, dict):
            results = [results]
        if isinstance(results, list) and all([isinstance(i, dict) for i in results]):
            now = datetime.utcnow()
            for item in results:
                item[self.timestamp_attribute] = now
            logger.debug('Updating cache with {} documents'.format(len(results)))
            cache.insert(results)

    @classmethod
    def get_method_module(cls, fn):
        return inspect.getmodule(fn).__name__

    @classmethod
    def get_configuration(cls, location, attribute):
        try:
            return operator.attrgetter(location)(attribute)
        except AttributeError:
            logger.debug('{}.{} not in configuration'.format(cls.cache_config_path, attribute))
            return None


def document_cache(fn):
    """ Document Cache """
    cache = Cache(fn)

    def decorator(*args, **kwargs):
        cached_results = cache.get(*args, **kwargs)
        if cached_results:
            return cached_results
        output = fn(*args, **kwargs)
        cache.update(output)
        return output
    return update_wrapper(decorator, fn)
