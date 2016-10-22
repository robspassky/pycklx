# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pycklx',
    version='0.0.1',
    description='Translate xml file to pickle and vice-versa',
    long_description=readme,
    author='Rob Cabacungan',
    author_email='robspassky@gmail.com',
    url='https://github.com/robspassky/pycklx',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

