from setuptools import setup, find_packages

from discordex import (
    __version__ as version,
    __author__ as author,
    __license__ as _license,
    __name__ as name,
)

setup(
    name=name,
    version=version,
    license=_license,
    author=author,
    author_email="devkiki7000@gmail.com",
    description="discord.py extension",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Team-Kat/dex.py",
    packages=find_packages(),
    install_requires=open("requirements.txt").readlines(),
    python_requires=">=3.8",
)
