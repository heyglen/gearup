# -*- coding: utf-8 -*-

import os
import sys
import logging

from invoke import Program, Collection, task

from gear.versions import Version

from gear.collections import scp_collection
from gear.collections import ssh_collection
from gear.collections import git_collection
from gear.collections import versions_collection
from gear.collections import pytest_collection
from gear.collections.git_flow_collection import ns_git_flow

logger = logging.getLogger('nnit_nnmi.utility.invoke')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(name)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


@task()
def env(ctx):
    print 'hi'
    print ctx


@task(autoprint=True)
def directories(ctx, folder='.'):
    if sys.platform == 'win32':
        res = ctx.run('dir /AD /B {}'.format(folder))
    else:
        res = ctx.run("find {} -type d | sed -e 's|./||g' | grep -v '\.'".format(folder))
    dirs = res.stdout.split()
    return dirs


ns = Collection()
ns.add_task(env)
ns.add_collection(git_collection, name='git')
ns.add_collection(scp_collection, name='scp')
ns.add_collection(ssh_collection, name='ssh')
ns.add_collection(ns_git_flow, name='git_flow')
ns.add_collection(versions_collection, name='version')
ns.add_collection(pytest_collection, name='test')

ns.configure({
    # https://github.com/pyinvoke/invoke/issues/345
    'run': {
        'shell': os.environ.get('COMSPEC', os.environ.get('SHELL'))
    }
})


program = Program(namespace=ns, version=Version.current())
