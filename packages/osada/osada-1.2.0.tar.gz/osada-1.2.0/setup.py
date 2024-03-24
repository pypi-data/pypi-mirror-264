from setuptools import setup, find_packages

setup(
    name='osada',
    version='1.2.0',
    author='OSADA Masashi',
    packages=find_packages(),
    install_requires=[
        'sounddevice>=0.4.6',
    ],
)
