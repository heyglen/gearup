# -*- coding: utf-8 -*-

import logging

from invoke import task, Collection

from gearup.utils.operating_system import OperatingSystem


logger = logging.getLogger(__name__)

        
        
@task(name='name')
def get_os_name(ctx):
    return OperatingSystem.name()
    
