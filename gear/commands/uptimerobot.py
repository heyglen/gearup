# -*- coding: utf-8 -*-

import ijson
import logging
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import click
import requests
import pandas as pnd
import matplotlib.pyplot as plt


from gear.utils.credentials import Credentials

plt.style.use('fivethirtyeight')


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
    def _clean_response_data(cls, data):
        return data.replace(u'jsonUptimeRobotApi(', u'').rstrip(u')')

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
    def _get_response(cls, monitor_id, cli=None):
        params = cls._get_params(cli, monitor_id)
        response = requests.get(
            '{}/{}'.format(cls._url, cls._methods.get('get')),
            params=params,
        )
        return response

    @classmethod
    def list(cls, cli=None):
        for monitor in cls._list_monitors(cli):
            # import ipdb; ipdb.set_trace()
            click.echo('{}: {}'.format(
                monitor.get('friendlyname'),
                monitor.get('id'),
            ))

    @classmethod
    def _list_monitors(cls, cli=None):
        url = '{}/{}'.format(cls._url, cls._methods.get('get'))
        params = cls._get_params(cli)
        response = requests.get(
            url,
            params=params,
        )
        data = cls._clean_response_data(response.text)
        data = StringIO(data)
        monitors = list()
        for monitor in ijson.items(data, 'monitors.monitor.item'):
            monitors.append(monitor)
        return monitors

    @classmethod
    def _get_monitor_id(cls, monitor, cli=None):
        monitor_id = None
        friendly_name = None
        for monitor_object in cls._list_monitors(cli):
            if monitor_object.get('friendlyname') == monitor or monitor_object.get('id') == monitor:
                monitor_id = monitor_object.get('id')
                friendly_name = monitor_object.get('friendlyname')
                break
        return monitor_id, friendly_name

    @classmethod
    def _graph(cls, monitor, cli=None, file_name=None):
        monitor_id, friendlyname = cls._get_monitor_id(monitor, cli=cli)
        response = cls._get_response(monitor_id, cli=cli)
        data = cls._clean_response_data(response.text)
        data = StringIO(data)

        dates = list()
        values = list()
        for measure in ijson.items(data, 'monitors.monitor.item.responsetime.item'):
            dates.append(measure.get('datetime'))
            values.append(int(measure.get('value')))

        index = pnd.to_datetime(dates, dayfirst=False)
        series = pnd.Series(values, index=index)
        ax = series.plot()
        ax.set_title('Response Time: {}'.format(friendlyname))
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
