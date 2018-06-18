from setuptools import setup, find_packages
import os

version = '0.0.1'

setup(
    name='epaas_com',
    version=version,
    description='EPAAS.com website',
    author='Dataent',
    author_email='info@epaas.com',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=("dataent",),
)
