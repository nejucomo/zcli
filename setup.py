#!/usr/bin/env python

from setuptools import setup, find_packages


PACKAGE = 'zcash_cli_helper'

setup(
    name=PACKAGE,
    description='Simply certain useful tasks on top of the Zcash RPC interface.',
    version='0.1',
    author='Nathan Wilcox',
    author_email='nejucomo+dev@gmail.com',
    license='GPLv3',
    url='https://github.com/nejucomo/{}'.format(PACKAGE),

    packages=find_packages(),

    entry_points={
        'console_scripts': [
            '{} = {}.main:main'.format(
                PACKAGE.replace('_', '-'),
                PACKAGE,
            )
        ],
    }
)
