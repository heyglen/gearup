# -*- coding: utf-8 -*-

import os
import logging
from contextlib import contextmanager

import click
import requests
from livereload import Server

from gear.commands.pip import Pip
from gear.commands.file_system import FileSystem


logger = logging.getLogger(__name__)


@contextmanager
def hidden_progress_bar(*args, **kwargs):
    pass


class Http(object):

    @classmethod
    def download(cls, cli, url, download_path=None, show_progress=True):
        Pip.install(cli, 'requests')
        if download_path is None:
            download_path = os.getcwd()
        else:
            download_path = FileSystem.get_directory(download_path)
        file_name = cls.get_url_filename(url)
        file_path = os.path.sep.join([download_path, file_name])
        domain_name = url.split('/')[2]
        response = requests.get(url)
        cls._verify_response(response)
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

    @classmethod
    def _verify_response(cls, response):
        if not response.ok:
            raise ValueError('Website returned code HTTP-{}'.format(response.status_code))

    @classmethod
    def get_url_filename(cls, url):
        return url.split('/')[-1].replace('%20', ' ')

    @classmethod
    def serve(cls, cli, file_path=None):
        Pip.install(cli, 'livereload')
        if file_path is None:
            file_path = os.getcwd()
        else:
            try:
                file_path = FileSystem.get_file(file_path)
            except ValueError:
                file_path = FileSystem.get_directory(file_path)
        server = Server()
        server.watch(file_path)
        logger.debug('Serving {}'.format(file_path))
        server.serve(root=file_path)
