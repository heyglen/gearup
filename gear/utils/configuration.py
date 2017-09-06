
import base64
import copy
import os
import pathlib
import logging

import appdirs
import yaml

from gear.utils.dot_dict import DotDict

logger = logging.getLogger(__name__)

APP_AUTHOR = 'GlenHarmon'
MODULE_NAME = __name__.split('.')[0]

default_configuration = {
    'log': {
        'level': 'debug',
    },
    'cisco': {
        'psirt' :{
            'username': None,
            'password': None,
        },
        'eox' :{
            'username': None,
            'password': None,
        },
    },
    'uptimerobot': {
        'api': {
            'client_id': None,
            'key': None,
        }
    }
}

configuration = copy.deepcopy(default_configuration)

configuration_directory = pathlib.Path(appdirs.user_config_dir(MODULE_NAME, APP_AUTHOR))
configuration_path = configuration_directory / 'configuration.yml'

if configuration_directory.is_dir():
    if configuration_path.is_file():
        with open(configuration_path) as f:
            loaded_config = yaml.safe_load(f) or dict()
            configuration.update(loaded_config)
            logger.debug(f'Loaded configuration file {configuration_path}')

def _get_env(name, cls_type=str, decode=False):
    value = os.environ.get(name)
    if value and cls_type is not None:
        value = cls_type(value)
    if isinstance(value, str) and decode:
        value = base64.b64decode(value)
    if value is not None:
        if decode:
            logger.debug(f'Loaded environment vairable {name}')
        else:
            logger.debug(f'Loaded environment vairable {name}={value}')
    return value

def clean_config(config):
    new_dict = dict()
    for key, value in config.items():
        if isinstance(value, dict):
            value = clean_config(value)
            if value:
                new_dict[key] = value
        elif value is not None:
            new_dict[key] = value
    return new_dict


environment_configuration = {
    'cisco': {
        'psirt' :{
            'username': _get_env('GEAR_CISCO_PSIRT_USERNAME'),
            'password': _get_env('GEAR_CISCO_PSIRT_PASSWORD', decode=True),
        },
        'eox' :{
            'username': _get_env('GEAR_CISCO_EOX_USERNAME'),
            'password': _get_env('GEAR_CISCO_EOX_PASSWORD', decode=True),
        },
    },
    'uptimerobot': {
        'api': {
            'client_id': _get_env('GEAR_UPTIMEROBOT_USERNAME'),
            'key': _get_env('GEAR_UPTIMEROBOT_KEY', decode=True),
        }
    }
}

environment_configuration = clean_config(environment_configuration)
configuration.update(environment_configuration)

configuration['log']['level'] = getattr(logging, configuration['log']['level'].upper())

configuration = DotDict(configuration)