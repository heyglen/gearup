#!/usr/local/bin/python3

import json
import logging
from datetime import datetime

import click
import requests
import oauth2 as oauth
from invoke.config import Config

from gearup.utils.credentials import Credentials

logger = logging.getLogger(__name__)


class Psirt(object):
    _token_url = 'https://cloudsso.cisco.com/as/token.oauth2?grant_type=client_credentials&client_id={}&client_secret={}'
    _advisories_url = 'https://api.cisco.com/security/advisories/cvrf/year/{}'

    def __init__(self):
        self._credentials = Credentials('cisco.api.psirt')
        self._session = requests.Session()

    def _get_headers(self):
        if not hasattr(self, '_headers'):
            logger.debug('Building request headers')
            access_token = self._get_access_token()
            self._headers = {
                'Accept': 'application/json',
                'Authorization' : 'Bearer {}'.format(access_token)
            }
        return self._headers

    def _get_access_token(self):
        if not hasattr(self, '_access_token'):
            logger.debug('Authenticating')
            username = self._credentials.username
            password = self._credentials.password
            consumer = oauth.Consumer(key=username,secret=password)
            request_token_url = self._token_url.format(username, password)
            client = oauth.Client(consumer)

            response = self._session.post(request_token_url)
            logger.debug(response.text)
            data = response.json()
            self._access_token = data['access_token']
            logger.debug('Access Token Retrieved')
        return self._access_token

    def _get(self, url):
        # Replace the Request URL below with the openVuln REST API resource you would like to access.
        # In this example, we are getting all advisories in CVRF format
        # The available resources are documented at:
        # https://developer.cisco.com/site/PSIRT/get-started/getting-started.gsp

        headers = self._get_headers()
        response = self._session.get(url, headers=headers)
        return response.json()

    def get_advisories(self, year=None):
        if year is None:
            year = datetime.now().year
        logger.debug('Getting advisories for {}'.format(year))
        data = self._get(self._advisories_url.format(year))
        return data['advisories']
