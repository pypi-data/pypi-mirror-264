from setuptools import setup, find_packages

VERSION = '1.10'

setup(
    name='kalamari-cli',
    version=VERSION,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'kalamari=kalamari:kalamari',
        ],
    },
    author='Sentou Technologies',
    author_email='hello@sentou.tech',
    description='Kalamari CLI tool for smart contract management and development.',
    install_requires=[
        'argparse',
    ],
)