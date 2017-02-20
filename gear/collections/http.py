# -*- coding: utf-8 -*-

import logging

from invoke import task

from gear.commands.http import Http


logger = logging.getLogger(__name__)


@task()
def download(ctx, url, download_path=None, show_progress=True):
    return Http.download(ctx, url, download_path, show_progress)


@task()
def serve(ctx, file_path):
    Http.serve(ctx, file_path)
