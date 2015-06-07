#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

VERSION = '2.0.0'

setup(
    name='entweet',
    version=VERSION,
    description='Security and verification for Twitter',
    long_description=open('README.rst').read(),
    author='David Gouldin and Cory Benfield',
    author_email='cory@lukasa.co.uk',
    url='http://lukasa.co.uk/',
    packages=['entweet'],
    package_dir={'entweet': 'entweet'},
    install_requires=[
        'Click~=4.0',
        'Pillow~=2.8.1',
        'python-gnupg~=0.3.7',
        'requests-oauthlib~=0.5.0'
    ],
    entry_points='''
        [console_scripts]
        entweet=entweet.entweet:cli
    ''',
    package_data={'entweet': ['Inconsolata-Regular.ttf']},
    include_package_data=True,
    license='MIT',
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ),
)
