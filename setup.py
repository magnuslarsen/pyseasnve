#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["requests>=2.7", "pytz>=2021.3"]
test_requirements = []

setup(
    author="Magnus Larsen",
    author_email="magnusfynbo@hotmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="An unofficial class to interact with the Seas-NVE API",
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="pyseasnve",
    name="pyseasnve",
    packages=find_packages(include=["pyseasnve", "pyseasnve.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/magnuslarsen/pyseasnve",
    version="0.2.0",
    zip_safe=False,
)
