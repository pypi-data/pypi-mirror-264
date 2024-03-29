from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='PlutoAuth',
    version='1.0.2',
    description='Official API Wrapper for Pluto Authentication (https://pluto-mc.net)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Pluto Development Team',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pydantic',
    ],
)