from setuptools import setup, find_packages

setup(
    name='PlutoAuth',
    version='1.0.0',
    description='Official API Wrapper for Pluto Authentication (https://pluto-mc.net)',
    author='Pluto Development Team',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pydantic',
    ],
)