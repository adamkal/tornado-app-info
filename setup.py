#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='tornado-app-info',
    version='0.1.0',
    description='Captures info about the state of application awhen application is loaded. That information might be useful to check which version of app is being used to serve the content',
    long_description=readme + '\n\n' + history,
    author='Adam Kaliński',
    author_email='adam.kalinski@gmail.com',
    url='https://github.com/adamkal/tornado-app-info',
    packages=[
        'tornado-app-info',
    ],
    package_dir={'tornado-app-info': 'tornado-app-info'},
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='tornado-app-info',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)