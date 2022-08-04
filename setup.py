# -*- coding: utf-8 -*-

import os
import setuptools
import sys

requirements = ['pysocks']
if os.name == 'nt' and sys.version_info < (3, 0):
    requirements.append('win-inet-pton')

setuptools.setup(
    name='pync',
    version='0.17.0',
    author='Brendon Worthington',
    description='arbitrary TCP and UDP connections and listens (Netcat for Python).',
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    python_requires=">=2.7",
    entry_points={
        'console_scripts': ['pync=pync.__main__:main'],
    },
    install_requires=requirements,
)

