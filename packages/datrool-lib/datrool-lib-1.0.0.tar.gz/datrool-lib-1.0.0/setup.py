# -*- coding: utf-8 -*-
from setuptools import setup
__version__ = "1.0.0"


with open("README.md", "r") as fh:
	long_description = fh.read()

with open("requirements.txt", "r") as rq:
	required = rq.read().splitlines()


setup(
	name="datrool-lib",
	version=__version__,
	author="Patrik Katrenak",
	author_email="patrik@katryapps.com",
	description="Common library for the datrool project",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://gitlab.com/datrool/core/lib",

	package_dir={"CP_lib": "src"},
	include_package_data=True,

	install_requires=required,
	classifiers=[
		"Programming Language :: Python :: 3",
		"Operating System :: OS Independent",
		"Natural Language :: English",
	],
	platforms=["any"],
	python_requires=">=3.10",
)
