# -*- coding: utf-8 -*-

import logging
import datetime

import requests
# import oauth2 as oauth

from gear.utils.configuration import configuration
from gear.utils.dot_dict import DotDict

logger = logging.getLogger(__name__)


class Psirt(object):
    """
        https://developer.cisco.com/site/PSIRT/get-started/getting-started.gsp
        https://api.apis.guru/v2/specs/cisco.com/0.0.3/swagger.yaml
    """
    _advisory_standard = 'cvrf'  # 'oval'
    _token_url = 'https://cloudsso.cisco.com/as/token.oauth2'
    _base_url = 'https://api.cisco.com/security/advisories'

    def __init__(self):
        self._session = requests.Session()

    def _build_url(self, suffix):
        return '{}/{}/{}'.format(
            self._base_url,
            self._advisory_standard,
            suffix
        )

    def _get_headers(self):
        if not hasattr(self, '_headers'):
            logger.debug('Building request headers')
            access_token = self._get_access_token()
            self._headers = {
                'Accept': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
        return self._headers

    def _get_access_token(self):
        if not hasattr(self, '_access_token'):
            logger.debug('Authenticating')
            params = {
                'client_id': configuration.cisco.psirt.username,
                'client_secret': configuration.cisco.psirt.password
            }
            data = {'grant_type': 'client_credentials'}

            # consumer = oauth.Consumer(key=username, secret=password)
            # request_token_url = self._token_url.format(username, password)
            # oauth.Client(consumer)

            response = self._session.post(
                self._token_url,
                params=params,
                data=data,
            )
            response.raise_for_status()
            logger.debug(response.text.strip())
            self._access_token = response.json()['access_token']
            logger.debug('Access Token Retrieved')
        return self._access_token

    def _get(self, url):
        # Replace the Request URL below with the openVuln REST API resource you would like to access
        # In this example, we are getting all advisories in CVRF format
        # The available resources are documented at:
        # https://developer.cisco.com/site/PSIRT/get-started/getting-started.gsp

        headers = self._get_headers()
        logger.debug(f'GET {url}')
        logger.debug(f'headers: {headers}')
        response = self._session.get(url, headers=headers)
        logger.debug(f'Response: {response.text}')
        return response.json()

    def get(self, item):
        advisory = None
        if item.startswith('CVE'):
            logger.debug('Getting CVE advisory {}'.format(item))
            url = self._build_url('cve/{}'.format(item))
            advisory = self._get(url).get('advisories')
        else:
            logger.debug('Getting advisory client_id {}'.format(item))
            url = self._build_url('advisory/{}'.format(item))
            advisory = self._get(url).get('advisories')
        return advisory

    def list(self, critical=True, high=True, medium=None, low=None):
        advisories = list()
        levels = {
            'critical': critical,
            'high': high,
            'medium': medium,
            'low': low,
        }

        now = datetime.datetime.now()
        week_ago = now - datetime.timedelta(days=7)
        start_date = f'{week_ago.year}-{week_ago.month}-{week_ago.day}'
        end_date = f'{now.year}-{now.month}-{now.day}'

        advisories = list()
        for level_name, level_enabled in levels.items():
            if level_enabled:
                message = f'Getting {level_name} advisories since {start_date}'
                logger.debug(message)
                url = self._build_url(f'severity/{level_name}')
                params = {
                    'startDate': start_date,
                    'endDate': end_date,
                    'pageIndex': 1,
                    'pageSize': 5,
                }
                response = self._session.get(
                    url,
                    headers=self._get_headers(),
                    params=params,
                )
                response.raise_for_status()
                for advisory in response.json()['advisories']:
                    advisories.append(DotDict(advisory))
        return advisories
