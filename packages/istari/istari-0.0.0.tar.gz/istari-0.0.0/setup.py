from setuptools import setup, find_packages

setup(
    name='istari',
    version='0.0.0',
    author='Janus Digital LLC',
    author_email='justice@janusdigital.io',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'istari=istari.cli:main',
        ],
    }
)
