# -*- coding: utf-8 -*-

import logging

import pytest
from invoke import task

logger = logging.getLogger(__name__)


@task(name='all')
def all(ctx):
    pytest.main('')


@task(name='unit')
def unit(ctx):
    pytest.main('tests/unit')


@task(name='integration')
def integration(ctx):
    pytest.main('tests/unit')
