from setuptools import setup, find_packages
setup(
name='epiccrypto',
version='0.1.2.7',
author='Epic099',
author_email='',
description='Encryption is cool',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
install_requires=[
    "epicfilemanager"   
]
)