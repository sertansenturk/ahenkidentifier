#!/usr/bin/env python

from setuptools import setup

setup(name='ahenkidentifier',
    version='1.2.1',
    author='Sertan Senturk',
    author_email='contact AT sertansenturk DOT com',
    license='agpl 3.0',
    description='Identifies the ahenk (transposition) of a makam music recording given the tonic frequency and the symbol (or the makam)',
    url='http://sertansenturk.com',
    packages=['ahenkidentifier'],
    include_package_data=True,
    install_requires=[
        "numpy",
        "future",
    ],
)
