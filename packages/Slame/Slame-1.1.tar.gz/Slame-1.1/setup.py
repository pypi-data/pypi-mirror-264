#!/usr/bin/env python

from setuptools import setup

"""
:authors: ZHRXXgroup
:license: MIT License, see LICENSE file
:copyright: (c) 2024 ZHRXXgroup
"""

version = '1.1'

long_description = '''
Python module for serving a web server with built-in User System (login/register)
'''


setup(
    name="Slame",
    version=version,
    
    author='ZHRXXgroup',
    author_email="info@zhrxxgroup.com",

    description='''Python module for serving a web server and more''',
    long_description=long_description,

    url="https://github.com/zhrexx/Slame/",
    download_url="https://github.com/zhrexx/Slame/archive/{}.zip".format(version),

    license="MIT License, see LICENSE file",

    packages=['Slame'],
    install_requires=[],

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3'
    ]
)
