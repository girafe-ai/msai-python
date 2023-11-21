import os

from setuptools import setup  # type: ignore

from simple_math.__version__ import __version__


def read_requirements(filepath):
    reqs = []
    with open(filepath) as fp:
        for line in fp:
            reqs.append(line.strip())
    return reqs


setup(
    name="simple_math",
    version=__version__,
    description="A simple math package",
    author="John Doe",
    author_email="john@gmail.com",
    license="MIT",
    packages=["simple_math"],
    entry_points={
        "console_scripts": ["simple_math = simple_math.__main__:main"]
    },
    install_requires=read_requirements("requirements.txt"),
)
