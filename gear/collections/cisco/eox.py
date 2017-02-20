# -*- coding: utf-8 -*-

import logging

from invoke import task

from gear.commands.cisco.eox import CiscoHelloApi

logger = logging.getLogger(__name__)


@task(default=True)
def hello(ctx):
	CiscoHelloApi().hello_api_call()