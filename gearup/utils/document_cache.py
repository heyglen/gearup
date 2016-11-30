# -*- coding: utf-8 -*-

import inspect
import cPickle as pickle
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
        self.module = self.get_method_module(self.fn)
        module_db = self.module.replace('.', '_')

        uri = self.get_configuration('cache.document.db.mongodb', 'uri')
        uri = uri or 'mongodb://localhost:27017'

        client = MongoClient(uri)
        self.database = client[module_db]
        logger.debug('Loaded cache db: {}'.format(module_db))

    def get_cache_expire(self):
        timeout = self.get_configuration('cache.document.db', 'timeout')
        timeout = (timeout or self.default_cache_timeout_hours) * -1  # In hours, one week default
        return datetime.utcnow() - timedelta(hours=timeout)

    def get_database(self):
        return self.database[self.fn.func_name]

    def get_record_id(self, *args, **kwargs):
        return hash(pickle.dumps((args, kwargs)))

    def purge_all(self):
        cache = self.get_database()
        result = cache.delete_many({})
        logger.debug('Purged {} documents'.format(result.deleted_count))

    def purge_expired(self):
        cache = self.get_database()
        result = cache.delete_many({
            self.timestamp_attribute: {'$lt': self.get_cache_expire()}
        })
        logger.debug('Purged {} expired documents'.format(result.deleted_count))

    def get(self, *args, **kwargs):
        results = None
        cache = self.get_database()
        search = {
            self.record_id_attribute: self.get_record_id(*args, **kwargs),
            self.timestamp_attribute: {'$gt': self.get_cache_expire()}
        }
        result_set = cache.find(search)
        result_count = result_set.count()
        if result_count:
            logger.debug('{}.{} returning {} cached results'.format(
                self.module,
                self.fn.func_name,
                result_count
            ))
            results = pickle.loads(result_set.value)
        return results

    def update(self, value, *args, **kwargs):
        cache = self.get_database()
        cache.insert({
            self.record_id_attribute: self.get_record_id(*args, **kwargs),
            'value': pickle.dumps(value),
            self.timestamp_attribute: datetime.utcnow(),
        })
        logger.debug('Cache updated')

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
        cache.purge_expired()
        cache.update(output)
        return output
    return update_wrapper(decorator, fn)
