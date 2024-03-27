# setup.py

from setuptools import setup, find_packages

setup(
    name='dummy-api-package',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        dummy-api=dummy_api:cli
    ''',
    author='Your Name',
    author_email='your.email@example.com',
    description='A Python package to generate a dummy API template',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/dummy-api-package',
)
