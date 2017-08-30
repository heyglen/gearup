# -*- coding: utf-8 -*-

import json
import logging
from datetime import datetime

import click
import requests
from invoke.config import Config

from gear.commands.oauth.oauthv1 import Oauthv1
# from gear.commands.oauth.oauthv2 import Oauthv2

logger = logging.getLogger(__name__)


class Oauth(object):

    @classmethod
    def get(cls, appplication_name, version=1, token_url):
        if version is 1:
            return Oauthv1(appplication_name)
        # else:
        #     return Oauthv2(appplication_name)
