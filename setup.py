from os import environ
from setuptools import setup, find_packages

from discordex import __version__ as version

setup(
    name = 'dex.py',
    version = version,
    license = 'MIT',
    author = 'kiki7000',
    author_email = 'devkiki7000@gmail.com',
    description = 'discord.py extension',
    long_description = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/kiki7000/dex.py',
    packages = find_packages(),
    install_requires = open('requirements.txt').readlines(),
    python_requires = '>=3.8'
)