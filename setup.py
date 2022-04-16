# -*- coding: utf-8 -*-

import setuptools

setuptools.setup(
    name='pync',
    version='0.3.0',
    author='Brendon Worthington',
    description='arbitrary TCP and UDP connections and listens (Netcat for Python).',
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    python_requires=">=2.7",
    entry_points={
        'console_scripts': ['pync=pync.__main__:main'],
    },
)

