# -*- coding: UTF-8 -*-
from setuptools import setup
import setuptools

#with open("README.md", "r") as fh:
#    long_description = fh.read()


setup(
    name='pytrafficcontrol',
    version='1.0.03',
    packages=setuptools.find_packages(),
    url='',
    license='MIT',
    author=' MA JIANLI',
    author_email='majianli@corp.netease.com',
    description='A toolchain for simulating weak network conditions',
    long_description="",
    #long_description_content_type="text/markdown",
    install_requires=[
    'paramiko',
    'requests',
    'APScheduler'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    data_files=[],

    python_requires='>=3.7',
)



