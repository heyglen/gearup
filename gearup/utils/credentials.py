# -*- coding: utf-8 -*-

import operator
import base64
import logging
import getpass

import click
from invoke.config import Config

logger = logging.getLogger(__name__)


class Credentials(object):
    """ Credentials """

    def __init__(self, app, username=None, password=None):
        self.app = app
        self._username = username
        self._password = password
        self._config = Config()

    @property
    def client_key(self):
        return self.username

    @property
    def client_id(self):
        return self.username

    @property
    def client_secret(self):
        return self.password

    @property
    def username(self):
        if self._username is None:
            try:
                self._username = operator.attrgetter(self.app)(self._config).client_id
            except AttributeError:
                logger.debug('{}.username not in configuration'.format(self.app))
                self._username = click.prompt(
                    '{} username:'.format(self.app),
                    default=getpass.getuser(),
                    type=unicode,
                )
        return self._username

    @property
    def password(self):
        if self._password is None:
            try:
                password = operator.attrgetter(self.app)(self._config).client_secret
                self._password = base64.b64decode(password).strip()
            except AttributeError:
                logger.debug('{}.password not in configuration'.format(self.app))
                self._password = click.prompt(
                    '{} password:'.format(self.app),
                    type=unicode,
                )
        return self._password

    def __repr__(self):
        return '<{} {}: {}>'.format(
            self.__class__.__name__,
            self.app,
            self.username,
        )
