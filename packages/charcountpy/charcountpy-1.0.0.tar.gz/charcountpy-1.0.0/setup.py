from setuptools import setup, find_packages

setup(
    name='charcountpy',
    version='1.0.0',
    author='Mykola Karandiei',
    author_email='korondei@gmail.com',
    description='A Python package for counting single characters in given string',
    packages=find_packages(),
    install_requires=[
        'argparse'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
