from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='spacestudio-constellation',
    version='3.4.0',
    description='spacestudio™ constellation scripting API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Exotrail',
    author_email="support.spacestudio@exotrail.com",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python :: 3'
    ],
    keywords='spacestudio constellation scripting propulsion',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['requests', 'pyjwt', 'openpyxl', 'python-dotenv', 'numpy', 'matplotlib']
)
