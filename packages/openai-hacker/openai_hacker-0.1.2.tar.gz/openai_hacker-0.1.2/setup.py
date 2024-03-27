# -*- coding:utf-8 -*-

from __future__ import absolute_import

import os
import re

from setuptools import find_packages
from setuptools import setup


def read_requirements(file_path='requirements.txt'):
    if not os.path.exists(file_path):
        return []

    with open(file_path, 'r')as f:
        lines = f.readlines()

    lines = [x.strip('\n').strip(' ') for x in lines]
    lines = list(filter(lambda x: len(x) > 0 and not x.startswith('#'), lines))

    return lines


def read_description(file_path='README.md'):
    with open(file_path, encoding='utf-8') as f:
        desc = f.read()
    return desc


home_url = 'https://github.com/lixf/openai-hacker'
name = 'openai_hacker'

version = re.findall(r'''__version__.*['"](.+)['"]''', open(f'{name}/__init__.py').read(), flags=re.S)[0]

MIN_PYTHON_VERSION = '>=3.8'

long_description = read_description()
requires = read_requirements()
# extras_require = read_extra_requirements()

setup(
    name=name,
    version=version,
    description='hacker of openai python client',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=home_url,
    author='DataCanvas Community',
    author_email='lixf@sovon.net',
    license='Apache License 2.0',
    install_requires=requires,
    python_requires=MIN_PYTHON_VERSION,
    # extras_require=extras_require,
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(exclude=('docs', 'tests*')),
    # package_data={
    # },
    # entry_points={
    # },
    zip_safe=False,
    # include_package_data=True,
)
