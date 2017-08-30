# -*- coding: utf-8 -*-

import inspect
import pickle
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
    record_id_attribute = 'record_id'
    timestamp_attribute = 'cache_timestamp'
    cache_config_path = 'cache.document.db.mongodb'
    default_cache_timeout_hours = 168

    def __init__(self, fn):
        self.fn = fn
        self.module = self._get_method_module(self.fn)
        module_db = self.module.replace('.', '_')

        uri = self._get_configuration('cache.document.db.mongodb', 'uri')
        uri = uri or 'mongodb://localhost:27017'

        client = MongoClient(uri)
        self.database = client[module_db]
        logger.debug('Loaded cache db: {}'.format(module_db))

    def _get_cache_expire(self):
        timeout = self._get_configuration('cache.document.db', 'timeout')
        timeout = (timeout or self.default_cache_timeout_hours) * -1  # In hours, one week default
        too_old = datetime.utcnow() - timedelta(hours=timeout)
        logger.debug('Cached expire timestamp: {}'.format(too_old))
        return too_old

    def _get_database(self):
        return self.database[self.fn.func_name]

    def _get_record_id(self, *args, **kwargs):
        return pickle.dumps((args, kwargs))

    @classmethod
    def _get_method_module(cls, fn):
        return inspect.getmodule(fn).__name__

    @classmethod
    def _get_configuration(cls, location, attribute):
        try:
            return operator.attrgetter(location)(attribute)
        except AttributeError:
            logger.debug('{}.{} not in configuration'.format(cls.cache_config_path, attribute))
            return None

    def _purge_expired(self):
        cache = self._get_database()
        result = cache.delete_many({
            self.timestamp_attribute: {'$gt': self._get_cache_expire()}
        })
        deleted = result.deleted_count
        if deleted:
            logger.debug('Purged {} expired documents'.format(deleted))

    def purge(self):
        cache = self._get_database()
        result = cache.delete_many({})
        logger.debug('Purged {} documents'.format(result.deleted_count))

    def get(self, *args, **kwargs):
        cached_result = None
        cache = self._get_database()
        search = {
            self.record_id_attribute: self._get_record_id(*args, **kwargs),
            self.timestamp_attribute: {'$gt': self._get_cache_expire()}
        }
        result_set = cache.find_one(search)
        result_returned = result_set is not None
        if result_returned:
            logger.debug('{}.{} returning cached result'.format(
                self.module,
                self.fn.func_name,
            ))
            cached_result = pickle.loads(result_set.value)
        return (result_returned, cached_result)

    def update(self, value, *args, **kwargs):
        cache = self._get_database()
        cache.insert({
            self.record_id_attribute: self._get_record_id(*args, **kwargs),
            'value': pickle.dumps(value),
            self.timestamp_attribute: datetime.utcnow(),
        })
        self._purge_expired()
        logger.debug('Cache updated')


def document_cache(fn):
    """ Document Cache """
    cache = Cache(fn)

    def decorator(*args, **kwargs):
        result_returned, cached_result = cache.get(*args, **kwargs)
        if result_returned:
            return cached_result
        output = fn(*args, **kwargs)
        cache.update(output)
        return output
    return update_wrapper(decorator, fn)
