
import sys
import pathlib

import yaml

class DotDict(dict):
    """dot.notation access to dictionary attributes"""
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __getattr__(*args):
        val = dict.get(*args)
        return DotDict(val) if type(val) is dict else val

configuration = DotDict({
    'cisco': {
        'psirt' :{
            'username': '',
            'password': '',
        },
        'eox' :{

        },
    },
    'uptimerobot': {
        'api': {
            'client_id': '',
            'key': '',
        }
    }
})

configuration_path = DotDict()
configuration_path.win32 = pathlib.Path.home() / 'AppData' / 'Roaming'
configuration_path.linux = pathlib.Path.home() / '.config'

path = configuration_path[sys.platform] / 'gear'

if path.is_dir():
    path = path / 'configuration.yml'
    if path.is_file():
        with open(path) as f:
            loaded_config = yaml.safe_load(f) or dict()
            configuration.update(loaded_config)