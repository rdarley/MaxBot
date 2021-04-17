from setuptools import setup

import src

requirements = []
with open('requirements.txt') as f:
  requirements = f.read().splitlines()

readme = ''
with open('README.md') as f:
    readme = f.read()

setup(
    name='MaxBot',
    version=src.__version__,
    description='My personal Discord Bot to help me out',
    long_description=readme,
    url='https://github.com/rdarley/MaxBot',
    packages=['src', 'src.cogs', 'src.database'],
    python_requires='>=3.8.0'
)