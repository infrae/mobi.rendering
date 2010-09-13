#!/usr/bin/env python

from setuptools import setup, find_packages
import os

version="1.0"

setup(name='mobi.rendering',
      version=version,
      description='Mobile rendering library',
      author='Infrae',
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      author_email='info@infrae.com',
      url='http://mobi.infrae.com/',
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
