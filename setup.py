# pylint: skip-file
from setuptools import find_packages, setup

setup(
    name='WordleSolver',
    version='1.3',
    description='A Wordle solver with multiple strategies',
    author='Arun K Viswanathan',
    author_email='github@element77.com',
    url='https://github.com/arunkv/wordle',
    packages=find_packages(),
    install_requires=[
        'nltk',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.12',
    ],
)