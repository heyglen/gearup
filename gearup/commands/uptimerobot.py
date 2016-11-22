# -*- coding: utf-8 -*-

import sys
import logging
import platform
from StringIO import StringIO 

import click
import ijson
import requests
import pandas as pd
# import matplotlib


# matplotlib.style.use('ggplot')


logger = logging.getLogger(__name__)


class UpTimeRobot(object):
    _url = 'https://api.uptimerobot.com'
    _methods = {
        'get': 'getMonitors',
    }

    @classmethod
    def _get_response_json(cls, response):
        data = response.text.replace(u'jsonUptimeRobotApi(', u'').rstrip(u')')
        data = StringIO(data)
        return data


    @classmethod
    def _get_api_key(cls, cli):
        return cli.config.monitoring.sources.uptimerobot.apikey.main

    @classmethod
    def _get_params(cls, cli, monitor_id=None):
        params = {
            'apiKey': cls._get_api_key(cli),
            'responseTimes': 1,
            'showTimezone': 1,
            'format': 'json',
            'offset': 0,
        }
        if monitor_id:
            params['monitors'] = monitor_id
        return params

    @classmethod
    def _get_responses(cls, cli, monitor_id):
        params = cls._get_params(cli, monitor_id)
        response = requests.get(
            '{}/{}'.format(cls._url, cls._methods.get('get')),
            params=params,
        )
        data = cls._get_response_json(response)
        for response in ijson.items(data, 'monitors.monitor.item.responsetime.item'):
            yield response


    @classmethod
    def list(cls, cli):
        for monitor in cls._list_monitors(cli):
            # import ipdb; ipdb.set_trace()
            click.echo('{}: {}'.format(
                monitor.get('friendlyname'),
                monitor.get('id'),
            ))

    @classmethod
    def _list_monitors(cls, cli):
        url = '{}/{}'.format(cls._url, cls._methods.get('get'))
        params = cls._get_params(cli)
        response = requests.get(
            url,
            params=params,
        )
        data = cls._get_response_json(response)
        monitors = list()
        for monitor in ijson.items(data, 'monitors.monitor.item'):
            yield monitor


    @classmethod
    def _get_monitor_id(cls, cli, monitor):
        for monitor_object in cls._list_monitors(cli):
            if monitor_object.get('friendlyname') == monitor:
                return monitor_object.get('id')         

    @classmethod
    def graph(cls, cli, monitor):
        monitor_id = cls._get_monitor_id(cli, monitor)
        for response in cls._get_responses(cli, monitor_id):
            click.echo('{}: {}'.format(
                response.get('datetime'),
                response.get('value'),
            ))