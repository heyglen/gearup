
import configparser
from collections import namedtuple
import os
import pathlib

import semver


class Version:
    _part_map = {
        'major': semver.bump_major,
        'minor': semver.bump_minor,
        'patch': semver.bump_patch,
    }

    @classmethod
    def _get_config(cls):
        directory = pathlib.Path()
        setup_config = str(directory / 'setup.cfg')
        config = configparser.ConfigParser()
        config.read(setup_config)
        return config

    @classmethod
    def current(cls):
        config = cls._get_config()
        return config['bumpversion']['current_version']

    @classmethod
    def major(cls):
        return cls.bump('major')

    @classmethod
    def minor(cls):
        return cls.bump('minor')

    @classmethod
    def patch(cls):
        return cls.bump('patch')

    @classmethod
    def bump(cls, part):
        part = part.lower()
        current_version = cls.current()
        new_version = cls._part_map[part](current_version)
        cls._bump(new_version)

    @classmethod
    def _bump(cls, new_version):
        for version_file in cls._get_files_to_update(new_version):
            old_text = version_file.path.read_text()
            new_text = old_text.replace(
                version_file.find,
                version_file.replace
            )
            version_file.path.write_text(new_text)

    @classmethod
    def _get_files_to_update(cls, new_version):
        current_version = cls.current()
        config = cls._get_config()
        config_file_prefix = 'bumpversion:file:'
        base_path = str(pathlib.Path())

        for section in config.sections():
            if section.startswith(config_file_prefix):
                path = section.replace(config_file_prefix, '')
                path = os.path.sep.join([base_path, path])
                path = pathlib.Path(path)

                find = config[section].get('find')
                replace = config[section].get('replace')

                if find:
                    find = find.format(current_version=current_version)
                else:
                    find = current_version
                if replace:
                    replace = replace.format(new_version=new_version)
                else:
                    replace = new_version
                yield namedtuple('VersionRepalce', 'path find replace')(
                    path=path,
                    find=find,
                    replace=replace,
                )
