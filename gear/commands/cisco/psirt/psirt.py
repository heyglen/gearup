# -*- coding: utf-8 -*-

import logging
from datetime import datetime

import requests
import oauth2 as oauth

from gear.utils.credentials import Credentials
from gear.utils.document_cache import document_cache

logger = logging.getLogger(__name__)


class Psirt(object):
    """
        https://developer.cisco.com/site/PSIRT/get-started/getting-started.gsp
        https://api.apis.guru/v2/specs/cisco.com/0.0.3/swagger.yaml
    """
    _advisory_standard = u'cvrf'  # 'oval'
    _token_url = u'https://cloudsso.cisco.com/as/token.oauth2?' \
                 u'grant_type=client_credentials&client_id={}&client_secret={}'
    _base_url = u'http://api.cisco.com/security/advisories'

    def __init__(self):
        self._credentials = Credentials(u'cisco.api.psirt')
        self._session = requests.Session()

    def _build_url(self, suffix):
        base = '{}/{}/{}'.format(self._base_url, self._advisory_standard, suffix)
        return base

    def _get_headers(self):
        if not hasattr(self, '_headers'):
            logger.debug('Building request headers')
            access_token = self._get_access_token()
            self._headers = {
                'Accept': u'application/json',
                'Authorization': u'Bearer {}'.format(access_token)
            }
        return self._headers

    def _get_access_token(self):
        if not hasattr(self, '_access_token'):
            logger.debug('Authenticating')
            username = self._credentials.username
            password = self._credentials.password
            consumer = oauth.Consumer(key=username, secret=password)
            request_token_url = self._token_url.format(username, password)
            oauth.Client(consumer)

            response = self._session.post(request_token_url)
            logger.debug(response.text)
            data = response.json()
            self._access_token = data['access_token']
            logger.debug('Access Token Retrieved')
        return self._access_token

    def _get(self, url):
        # Replace the Request URL below with the openVuln REST API resource you would like to access
        # In this example, we are getting all advisories in CVRF format
        # The available resources are documented at:
        # https://developer.cisco.com/site/PSIRT/get-started/getting-started.gsp

        headers = self._get_headers()
        response = self._session.get(url, headers=headers)
        import ipdb; ipdb.set_trace()
        return response.json()

    @document_cache
    def get(self, item):
        advisory = None
        if item.startswith('CVE'):
            logger.debug('Getting CVE advisory {}'.format(item))
            url = self._build_url(u'cve/{}'.format(item))
            advisory = self._get(url).get('advisories')
        else:
            logger.debug('Getting advisory client_id {}'.format(item))
            url = self._build_url(u'advisory/{}'.format(item))
            advisory = self._get(url).get('advisories')
        return advisory

    @document_cache
    def issues(self, year=None, critical=None, high=None, medium=None, low=None):
        advisories = list()
        levels = {
            'critical': critical,
            'high': high,
            'medium': medium,
            'low': low,
        }
        if year is None:
            match = False
            for level, value in levels.items():
                if value:
                    match = True
                    logger.debug(u'Getting {} advisories'.format(level))
                    url = self._build_url(u'severity/{}'.format(level))
                    advisories = advisories + self._get(url).get('advisories')
            if not match:
                year = datetime.now().year
        if year:
            logger.debug('Getting advisories for {}'.format(year))
            url = self._build_url(u'year/{}'.format(year))
            data = self._get(url)
            advisories = data.get('advisories')
        return advisories
