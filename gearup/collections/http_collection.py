# -*- coding: utf-8 -*-

import os
import logging
from contextlib import contextmanager

import click
import requests
from invoke import task, Collection


logger = logging.getLogger(__name__)

@contextmanager
def hidden_progress_bar(*args, **kwargs):
    pass


def _get_directory(path):
    if not path.endswith(os.path.sep):
        directories = path.split(os.path.sep)[:-1]
        path = os.path.sep.join(directories)
    if not os.path.isdir(path):
        raise ValueError('{}: Invalid Directory'.format(path))
    return path


def get_url_filename(url):
    return url.split('/')[-1].replace('%20', ' ')


def _verify_response(response):
    if not response.ok:
        raise ValueError('Website returned code HTTP-{}'.format(response.status_code))

@task()
def download(ctx, url, download_path=None, show_progress=True):
    return http_download(url, download_path, show_progress)


def http_download(url, download_path=None, show_progress=True):
    if download_path is None:
        download_path = os.getcwd()
    else:
        download_path = _get_directory(download_path)
    file_name = get_url_filename(url)
    file_path = os.path.sep.join([download_path, file_name])
    domain_name = url.split('/')[2]
    response = requests.get(url)
    _verify_response(response)
    progress_bar = hidden_progress_bar
    if show_progress:
        progress_bar = click.progressbar
    with open(file_path, 'wb') as handle:
        total_length = int(response.headers.get('content-length'))
        with progress_bar(
            response.iter_content(1024),
            length=total_length,
            label='Downloading \'{}\' from {}'.format(file_name, domain_name)
        ) as data:
            for block in data:
                handle.write(block)
    directory = os.sep.join(download_path.split(os.sep)[:-1])
    logger.debug('Downloaded to \'{}\''.format(directory))
    return file_path

