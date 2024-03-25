#!/usr/bin/env python

from distutils.core import setup
from pathlib import Path

source_directory = Path(__file__).parent
#long_description = (source_directory / "README.md").read_text()
readme = open(source_directory.joinpath("README.rst")).read()


setup(
    name="MMLToolbox",
    description="",
    long_description_content_type= 'text/x-rst',
    long_description=readme,
    #long_description_content_type='text/markdown',
    version="1.0.9",
    author="IGTE",  
    author_email="andreas.gschwentner@tugraz.at",
    url="https://www.tugraz.at/institute/igte/home/",
    packages=["MMLToolbox", "MMLToolbox.util", "MMLToolbox.coord", "MMLToolbox.optic", "MMLToolbox.pxi"],
    # include_package_data=True,
    # scripts=["bin/generate-ex"],
    keywords=["parameter", "identification", "measurements", "optimization"],
    install_requires=["numpy" ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
    ],
    )
