# -*- coding: UTF-8 -*-
"""
@IDE     ：PyCharm 
@Date    ：2024/3/24 10:56 
# @File    : setup.py.py
@Author  ：夜黎
"""
from setuptools import setup

setup(
    name='NumThe',
    version='1.1',
    description='some common Number Theory',
    author='夜黎',
    author_email='z2544427399@163.com',
    packages=['library'],
    install_requires=[
        'itertools',
        'abc'
    ],
)
