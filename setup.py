#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


# monkey patch os.link to force using symlinks
import os
del os.link

setup(name='PyContentBits',
    url='https://github.com/michalbachowski/pycontentbits',
    version='0.1.0',
    description='Python content repository',
    license='New BSD License',
    author='Michał Bachowski',
    author_email='michal@bachowski.pl',
    packages=['contentbits', 'contentbits.storage', 'contentbits.interface'],
    package_dir={'': 'src'},
    install_requires=['python_mimeparse >= 0.1.4', 'tornado >= 3.0.1', \
            'PyPromise==1.1.0'],
    dependency_links = ['http://github.com/michalbachowski/pypromise/archive/1.1.0.zip#egg=PyPromise-1.1.0'])
