# -*- coding: utf-8 -*-

import os
import time
import logging

from gearup.commands.pip import Pip
from watchdog.observers import Observer
from watchdog.events import FileModifiedEvent, DirModifiedEvent

from gearup.commands.file_system import FileSystem


logger = logging.getLogger(__name__)


class WatchDog(object):

    @classmethod
    def modified(cls, file_name, callback, recursive=False, **kwargs):
        Pip.upgrade('watchdog')
        event_handler = cls._get_handler(file_name, callback, **kwargs)
        message = 'Calling {}'.format(callback.__name__)
        if FileSystem.is_file(file_name):
            file_name = FileSystem.get_file(file_name)
            message = '{} when {} is modified'.format(message, file_name)
            recursive = False
            path = file_name
        elif FileSystem.is_directory(file_name):
            directory = FileSystem.get_directory(file_name)
            path = directory
            if recursive:
                message = '{} when {}{}.* is modified'.format(
                    message,
                    directory.rstrip(os.path.sep),
                    os.path.sep,
                )
            else:
                message = '{} when {} is modified'.format(message, directory)
        logger.debug(message)
        cls._scheduled_observe(event_handler, path, recursive)

    @classmethod
    def _scheduled_observe(cls, event_handler, path, recursive):
        observer = Observer()
        observer.schedule(event_handler, path=path, recursive=recursive)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    @classmethod
    def _get_handler(cls, file_name, callback, **kwargs):
        if FileSystem.is_file(file_name):
            class FileChangeHandler(FileModifiedEvent):
                def on_modified(self, event):
                    callback(**kwargs)
            return FileChangeHandler(file_name)
        elif FileSystem.is_directory(file_name):
            class DirectoryChangeHandler(DirModifiedEvent):
                def on_modified(self, event):
                    callback(**kwargs)
            return DirectoryChangeHandler(file_name)
        message = 'Invalid file or directory name "{}".'.format(file_name)
        logger.error(message)
        raise ValueError(message)
