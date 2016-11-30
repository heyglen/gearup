# -*- coding: utf-8 -*-

import logging
from StringIO import StringIO

import click
import ijson
import requests
import pandas as pnd
# import matplotlib

from gearup.utils.credentials import Credentials
from gearup.utils.document_cache import document_cache

# matplotlib.style.use('ggplot')


logger = logging.getLogger(__name__)


class UpTimeRobot(object):
    _url = 'https://api.uptimerobot.com'
    _methods = {
        'get': 'getMonitors',
    }
    _credentials = None

    @classmethod
    def _get_credentials(cls, cli=None):
        if cls._credentials is None:
            cls._credentials = Credentials(u'uptimerobot.api')
        return cls._credentials

    @classmethod
    def _get_response_json(cls, response):
        data = response.text.replace(u'jsonUptimeRobotApi(', u'').rstrip(u')')
        data = StringIO(data)
        return data

    @classmethod
    def _get_params(cls, cli, monitor_id=None):
        params = {
            'apiKey': cls._get_credentials(cli).client_secret,
            'responseTimes': 1,
            'showTimezone': 1,
            'format': 'json',
            'offset': 0,
        }
        if monitor_id:
            params['monitors'] = monitor_id
        return params

    @classmethod
    @document_cache
    def _get_raw_response(cls, monitor_id, cli=None):
        params = cls._get_params(cli, monitor_id)
        response = requests.get(
            '{}/{}'.format(cls._url, cls._methods.get('get')),
            params=params,
        )
        return response

    @classmethod
    def _get_response(cls, monitor_id, cli=None):
        response = cls._get_raw_response(monitor_id, cli=cli)
        data = cls._get_response_json(response)
        for response in ijson.items(data, 'monitors.monitor.item.responsetime.item'):
            yield response

    @classmethod
    def list(cls, cli=None):
        for monitor in cls._list_monitors(cli):
            # import ipdb; ipdb.set_trace()
            click.echo('{}: {}'.format(
                monitor.get('friendlyname'),
                monitor.get('id'),
            ))

    @classmethod
    @document_cache
    def _list_monitors(cls, cli=None):
        url = '{}/{}'.format(cls._url, cls._methods.get('get'))
        params = cls._get_params(cli)
        response = requests.get(
            url,
            params=params,
        )
        data = cls._get_response_json(response)
        monitors = list()
        for monitor in ijson.items(data, 'monitors.monitor.item'):
            monitors.append(monitor)
        return monitors

    @classmethod
    def _get_monitor_id(cls, monitor, cli=None):
        result = None
        for monitor_object in cls._list_monitors(cli):
            if monitor_object.get('friendlyname') == monitor:
                result = monitor_object.get('id')
                break
            elif monitor_object.get('id') == monitor:
                result = monitor_object.get('id')
                break
        return result

    @classmethod
    def _graph(cls, monitor, cli=None):
        monitor_id = cls._get_monitor_id(monitor, cli=cli)
        return cls._get_raw_response(monitor_id, cli=cli)

    @classmethod
    def graph(cls, monitor, cli=None):
        for response in cls._get_response(monitor, cli=cli):
            click.echo('{}: {}'.format(
                response.get('datetime'),
                response.get('value'),
            ))
