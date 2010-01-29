#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='playmobile.rendering',
      version='0.1dev',
      description='Mobile Device management',
      author='Infrae',
      author_email='info@infrae.com',
      url='infrae.com',
      packages=find_packages(),
      install_requires=[
        'zope.interface',
        'zope.schema',
        'zope.component',
        'playmobile.interfaces',
      ],
     )
