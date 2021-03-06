#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = [
    'GitPython',
    'semver',
    'pymongo',
    'invoke',
    'pytest',
    'requests',
    'click',
    'ijson',
    'livereload',
    'watchdog',
    'oauth2',
    'requests_oauthlib',
    'bumpversion',
    'pandas',
    'colorlog',
    'matplotlib',
    'pyyaml',
    'notify2',
    'appdirs',
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='gear',
    version='0.1.0',
    description="Task automation",
    long_description=readme + '\n\n' + history,
    author="Glen Harmon",
    author_email='ghar@nnit.com',
    packages=find_packages(exclude=['contrib', u'docs', u'tests']),
    entry_points={
        'console_scripts': [
            'gear = gear.main:program.run',
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='gear',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
