# -*- coding: utf-8 -*-

import ijson
import copy
import logging
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import click
import requests
import pandas as pnd
import matplotlib.pyplot as plt

from gear.utils.configuration import configuration

plt.style.use('fivethirtyeight')


logger = logging.getLogger(__name__)


class UpTimeRobot(object):
    _url = 'https://api.uptimerobot.com/v2'
    _methods = {
        'get': 'getMonitors',
    }
    _default_headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache"
    }
    _base_data = {
        'api_key': configuration.uptimerobot.api.key,
        'format': 'json',
    }

    @classmethod
    def _get_data(cls, extra=None):
        entries = list()
        extra = extra or dict()
        for key, value in cls._base_data.items():
            entries.append('='.join([key, str(value)]))
        for key, value in extra.items():
            entries.append('='.join([key, str(value)]))
        return '&'.join(entries)

    @classmethod
    def _clean_response_data(cls, data):
        return data.replace(u'jsonUptimeRobotApi(', u'').rstrip(u')')

    @classmethod
    def _get_response(cls, monitor_id, cli=None):
        data = cls._get_data({
            'logs': 1,
            'response_times': 1,
            'monitors': monitor_id,
        })
        headers = cls._default_headers
        response = requests.post(
            '{}/{}'.format(cls._url, cls._methods.get('get')),
            headers=headers,
            data=data,
        )
        return response

    @classmethod
    def list(cls, cli=None):
        for monitor in cls._list_monitors(cli):
            name = monitor.get('friendly_name')
            monitor_id = monitor.get('id')
            click.echo(f'{name}')

    @classmethod
    def _list_monitors(cls, cli=None):
        url = '{}/{}'.format(cls._url, cls._methods.get('get'))
        data = cls._get_data()
        headers = cls._default_headers
        logger.debug(f'POST {url}')
        logger.debug(f'headers {headers}')
        logger.debug(f'data {data}')
        response = requests.post(
            url,
            data=data,
            headers=headers,
        )
        logger.debug(f'Returned: {response.text}')
        data = cls._clean_response_data(response.text)
        data = StringIO(data)
        monitors = list()
        for monitor in ijson.items(data, 'monitors.item'):
            monitors.append(monitor)
        return monitors

    @classmethod
    def _get_monitor_id(cls, monitor, cli=None):
        monitor_id = None
        friendly_name = None
        for monitor_object in cls._list_monitors(cli):
            if monitor_object.get('friendly_name') == monitor or monitor_object.get('id') == monitor:
                monitor_id = monitor_object.get('id')
                friendly_name = monitor_object.get('friendly_name')
                break
        return monitor_id, friendly_name

    @classmethod
    def _graph(cls, monitor, cli=None, file_name=None):
        monitor_id, friendly_name = cls._get_monitor_id(monitor, cli=cli)
        response = cls._get_response(monitor_id, cli=cli)
        data = cls._clean_response_data(response.text)
        data = StringIO(data)

        dates = list()
        values = list()
        for measure in ijson.items(data, 'monitors.item.response_times.item'):
            dates.append(measure.get('datetime'))
            values.append(int(measure.get('value')))

        logger.debug(f'Response returned {len(values)} values')

        index = pnd.to_datetime(dates, unit='s', origin='unix')
        series = pnd.Series(values, index=index)
        ax = series.plot()
        ax.set_title('Response Time: {}'.format(friendly_name))
        ax.set_xlabel('Time')
        fig = ax.get_figure()
        if file_name is None:
            fig.show()
            plt.show()  # Wait for exit
        else:
            fig.savefig('{}.png'.format(file_name))
        return series

    @classmethod
    def graph(cls, monitor, cli=None, file_name=None):
        return cls._graph(monitor, cli=cli, file_name=file_name)
