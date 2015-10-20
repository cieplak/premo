#!/usr/bin/env python
from setuptools import setup


requirements = [
    'ansible',
    'boto3',
    'click',
    'coid',
    'flask',
    'ipython',
    'iso8601',
    'kombu',
    'pika',
    'pilo',
    'psycopg2',
    'sqlalchemy',
]


setup(
    name='premo',
    version='0.0.1',
    url='https://www.github.com/cieplak/premo',
    author='patrick cieplak',
    author_email='patrick.cieplak@gmail.com',
    description='premo utilities',
    packages=['premo'],
    license=open('LICENSE').read(),
    include_package_data=True,
    install_requires=requirements,
    tests_require=['faker', 'mock', 'nose', 'ipdb'],
    scripts=['bin/premo'],
)
