#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django-fprice',
    version='0.1',
    description='Price app for Django Web Framework',
    author='PF',
    author_email='dfalk@gmail.com',
    packages=find_packages(),
    include_package_data = True,
    # TODO install_requires=[''],
)

