import os

from setuptools import find_packages, setup


def read(filename: str) -> str:
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        return file.read()


def parse_requirements() -> tuple:
    """Parse requirements.txt for install_requires"""
    requirements = read('requirements.txt')
    return tuple(requirements.split('\n'))


setup(
    name='actions_example',
    packages=find_packages(exclude=('tests', )),
    python_requires='~=3.7',
    install_requires=parse_requirements(),
)