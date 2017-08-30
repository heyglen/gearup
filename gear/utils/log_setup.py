import logging

import colorlog


verbose_formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)-2s%(reset)s %(name)-3s %(white)s%(message)s",
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


def log_setup(name=None):
    name = name if name is not None else 'ucsd'
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.handlers = []
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(verbose_formatter)
        logger.addHandler(handler)
    return logger