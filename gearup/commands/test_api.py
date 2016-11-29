# -*- coding: utf-8 -*-

from gearup.commands.document_cache import document_cache


class TestApi(object):
    @document_cache
    def get(value=None):
        return 'worked'
