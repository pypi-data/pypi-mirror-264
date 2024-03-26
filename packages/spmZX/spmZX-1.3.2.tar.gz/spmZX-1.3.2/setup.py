#!/usr/bin/env python

from setuptools import setup

"""
:authors: ZHRXXgroup
:license: MIT License, see LICENSE file
:copyright: (c) 2024 ZHRXXgroup
"""

version = '1.3.2'

long_description  = "Slame is an Python Module for serving a webserver and in 1.2 we added Plugins you can use your own plugins in Slame or you can download plugins from other Peoples at https://zhrxxgroup.com/slame/spm/. SLAME DOCS: https://zhrxxgroup.com/slame or https://github.com/zhrexx/Slame, OUR WEBSITE: https://zhrxxgroup.com"



setup(
    name="spmZX",
    version=version,
    
    author='ZHRXXgroup',
    author_email="info@zhrxxgroup.com",

    description='''Python module for serving a web server and more''',
    long_description=long_description,

    url="https://github.com/zhrexx/Slame/",
    download_url="https://zhrxxgroup.com/slame/",

    license="MIT License, see LICENSE file",

    packages=['spmZX'],
    install_requires=["requests", "tqdm"],

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3'
    ]
)
