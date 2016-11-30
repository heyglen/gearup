# -*- coding: utf-8 -*-

import os


class MongoDb(object):
    log_file_name = '.mongodb.log'
    service_name = 'MongoDB'

    @staticmethod
    def install(cli):
        user_directory = os.path.expanduser('~')
        log_file_path = os.path.sep.join([user_directory, MongoDb.log_file_name])
        command = "mongod --install --serviceName {0} --serviceDisplayName {0}".format(
            MongoDb.service_name,
        )
        command = "{} --logpath {1} --logappend".format(
            command,
            log_file_path,
        )
        cli.run(command)

    @staticmethod
    def start(cli):
        output = cli.run('mongod')
        if 'waiting for connections on port' in output.stdout:
            return True
        raise SystemError('Unable to start mongodb. Error: \n{}'.format(output.stderr))
