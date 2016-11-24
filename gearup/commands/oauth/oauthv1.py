# -*- coding: utf-8 -*-

import json
import logging
from datetime import datetime

import click
import requests
import oauth2 as oauth
from invoke.config import Config
from requests_oauthlib import OAuth1Session

from gearup.utils.credentials import Credentials

logger = logging.getLogger(__name__)


class Oauthv1(object):

    def __init__(self, application_name, request_token_url, authorization_url,
                 autorization_redirect_url, access_token_url):
        self._credentials = Credentials(application_name)
        self._session = requests.Session()
        self._request_token_url = request_token_url
        self._authorization_url = authorization_url
        self._autorization_redirect_url = autorization_redirect_url
        self._access_token_url = access_token_url

    def get(self, url):
        self._oauth_process()
        session = OAuth1Session(
            self._credentials.client_key,
            client_secret=self._credentials.client_secret,
            resource_owner_key=self._resource_owner_key,
            resource_owner_secret=self._access_token,
        )
        return session.get(url)        

    def _oauth_process(self):
        if not hasattr(self, '_access_token'):
            self._get_request_token()
            self._get_verification()
            self._get_access_token()

    def _get_session(self):
        if not hasattr(self, '_session'):
            logger.debug('Getting OAuth session')
            client_key = self._credentials.client_key
            client_secret = self._credentials.client_secret
            self._session = OAuth1Session(client_key, client_secret=client_secret)
        return self._session        
            
    def _get_request_token(self):
        logger.debug('Getting request token')
        request_token_url = self._request_token_url
        oauth_session = self._get_session()
        response = oauth_session.fetch_request_token(request_token_url)
        self._resource_owner_key = response.get('oauth_token')
        self._resource_owner_secret = response.get('oauth_token_secret')

    def _get_verification(self):
        logger.debug('Getting verification')
        oauth_session = self._get_session()
        authorization_url = oauth_session.authorization_url(self._authorization_url)
        response = oauth.parse_authorization_response(self._autorization_redirect_url)
        self._verification = response.get('oauth_verifier')
        
    def _get_access_token(self):
        session = OAuth1Session(
            self._credentials.client_key,
            client_secret=self._credentials.client_secret,
            resource_owner_key=self._resource_owner_key,
            resource_owner_secret=self._resource_owner_secret,
            verifier=self._verification,
        )
        response = session.fetch_access_token(access_token_url)
        self._access_token = response.get('oauth_token_secret')
