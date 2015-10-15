# -*- coding: utf-8 -*-
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='illmatic',
    version='0.1',
    description='',
    author='',
    author_email='',
    entry_points="""
    [pecan.command]
    reset-db=illmatic.cmd.reset_db:GetCommand
    """,
    install_requires=[
        "pecan",
    ],
    test_suite='illmatic',
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(exclude=['ez_setup'])
)
