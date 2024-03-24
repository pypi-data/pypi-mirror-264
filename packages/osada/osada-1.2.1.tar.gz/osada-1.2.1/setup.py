import os
from setuptools import setup, find_packages

DIR = os.path.dirname(os.path.abspath(__file__))


with open(f'{DIR}/README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()


setup(
    name='osada',
    version='1.2.1',
    author='OSADA Masashi',
    author_email='osadamasashi.a@gmail.com',
    description='Packed with features that the author, Osada, wants to use.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Osada-M/osada',
    packages=find_packages(),
    install_requires=[
        'sounddevice>=0.4.6',
    ],
)
