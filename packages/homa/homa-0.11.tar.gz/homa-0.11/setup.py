from setuptools import setup
from setuptools import find_packages

with open("README.md") as fh:
    description = fh.read()

setup(
    name="homa",
    version="0.11",
    packages=find_packages(),
    install_requires=[
        #
    ],
    long_description=description,
    long_description_content_type="text/markdown"
)
