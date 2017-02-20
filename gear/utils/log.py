# -*- coding: utf-8 -*-

import logging
import sys

import colorlog


def log_setup(name):
    verbose_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)-2s%(reset)s %(white)s%(message)s",
        # "%(name)-3s %(log_color)s%(levelname)-2s%(reset)s %(white)s%(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )

    logger = logging.getLogger(name.split('.')[0])
    logger.handlers = list()
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(verbose_formatter)
    logger.addHandler(handler)
    return logger
