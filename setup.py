#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='mobi.rendering',
      version='0.1dev',
      description='Mobile Device management',
      author='Infrae',
      author_email='info@infrae.com',
      url='infrae.com',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      namespace_packages=['mobi'],
      install_requires=[
        'zope.interface',
        'zope.schema',
        'zope.component',
        'mobi.interfaces',
        'mobi.schema',
        'mobi.caching',
        'nose',
      ],
      test_suite='nose.collector',
     )
