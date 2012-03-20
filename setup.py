#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='django-better-emails',
	description='A Django app which sends activation and confirmation emails',	
	version='0.1',
	url='http://github.com/florentin/django-better-emails/',
	keywords='django',
	license='BSD',
    author='Florentin Sardan',
    author_email='florentindev@gmail.com',
    long_description=open('README.md', 'r').read(),
	zip_safe=False,
	platforms='any',	
	packages=find_packages(exclude=['tests', 'tests.*']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
		'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ],
)
