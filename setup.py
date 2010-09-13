#!/usr/bin/env python

from setuptools import setup, find_packages

version="1.0"


setup(name='mobi.rendering',
      version=version,
      description='Mobile Device management',
      author='Infrae',
      author_email='info@infrae.com',
      url='infrae.com',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      namespace_packages=['mobi'],
      install_requires=[
        'Chameleon',
        'zope.interface',
        'zope.schema',
        'zope.component',
        'mobi.interfaces',
        'mobi.caching',
      ],
      test_suite='nose.collector',
     )
