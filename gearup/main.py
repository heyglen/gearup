# -*- coding: utf-8 -*-

import os
import sys
import logging

from invoke import Program, Collection, task, Argument

from gearup.versions import Version

from gearup.collections import git as git_collection
from gearup.collections import git_flow as git_flow_collection
from gearup.collections import scp as scp_collection
from gearup.collections import ssh as ssh_collection
from gearup.collections import versions as versions_collection
from gearup.collections import pytest as pytest_collection
from gearup.collections import http as http_collection
from gearup.collections import files as files_collection
from gearup.collections import update as update_collection
from gearup.collections import pip as pip_collection
from gearup.collections import packages as packages_collection
from gearup.collections import monitors as monitors_collection
from gearup.collections import cisco as cisco_collection
from gearup.collections.cisco import eox as cisco_eox_collection
from gearup.collections.cisco import psirt as cisco_psirt_collection


logger = logging.getLogger('gearup')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(name)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


@task()
def env(ctx, default=True):
    import ipdb; ipdb.set_trace()


@task(autoprint=True)
def directories(ctx, folder='.'):
    if sys.platform == 'win32':
        directory_list = ctx.run('dir /AD /B {}'.format(folder))
    else:
        directory_list = ctx.run("find {} -type d | sed -e 's|./||g' | grep -v '\.'".format(folder))
    return directory_list.stdout.split()


namespace = Collection('gearup')
namespace.add_task(env, 'env')
namespace.add_collection(git_collection, name='git')
namespace.add_collection(scp_collection, name='scp')
namespace.add_collection(ssh_collection, name='ssh')
namespace.add_collection(git_flow_collection, name='git_flow')
namespace.add_collection(versions_collection, name='versions')
namespace.add_collection(pytest_collection, name='test')
namespace.add_collection(http_collection, name='http')
namespace.add_collection(files_collection, name='file')
namespace.add_collection(update_collection, name='update')
namespace.add_collection(pip_collection, name='pip')
namespace.add_collection(packages_collection, name='packages')
namespace.add_collection(monitors_collection, name='monitors')
cisco_collection = Collection()
namespace.add_collection(cisco_collection, name='cisco')
cisco_collection.add_collection(cisco_eox_collection, name='eox')
cisco_collection.add_collection(cisco_psirt_collection, name='advisories')

namespace.configure({
    # https://github.com/pyinvoke/invoke/issues/345
    'run': {
        'shell': os.environ.get('COMSPEC', os.environ.get('SHELL'))
    }
})


class MyProgram(Program):
    def core_args(self):
        core_args = super(MyProgram, self).core_args()
        extra_args = [
            # https://github.com/pyinvoke/invoke/issues/276
            Argument(
                names=('list', 'l'),
                kind=bool,
                default=False,
                help="List available tasks."
            ),
            Argument(
                names=['no-dedupe'],
                help="Define no-dedupe argument (does nothing)",
            ),
        ]
        return core_args + extra_args


program = MyProgram(
    namespace=namespace,
    binary='gearup',
    version=Version.current(),
)
