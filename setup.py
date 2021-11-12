# -*- coding: utf-8 -*-

import setuptools

setuptools.setup(
    name='pync',
    version='0.0.1',
    author='brenw0rth',
    description='An attempt at creating netcat with Python.',
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    python_requires=">=2.7",
    entry_points={
        'console_scripts': ['pync=pync.__main__:main'],
    },
)

