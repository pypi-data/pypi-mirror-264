# local
import pathlib
import os
from setuptools import setup, find_packages
# standard
# from depthcryption.version import __version__ as _dcv

with open(pathlib.Path(os.path.dirname(__file__)).joinpath('README.md'), 'r'
          ) as f:
    readme_contents = f.read()

setup(
    name='depthcryption',
    version='0.0.1.0',
    include_package_data=True,
    packages=find_packages(),
    package_data={"sls": ["*.pyc"]},
    python_requires='>=3.9',
    author='Mitchell Williams',
    url='',
    install_requires=[],
    description='A bleeding edge encryption package that offers a powerful '
                'never-before-seen approach to encryption with an impressive '
                'suite of features in easy to use functions.',
    long_description=readme_contents,
    long_description_content_type="text/markdown",
    license_files=['LICENSE.txt'],
)


