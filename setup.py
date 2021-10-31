"""GpgTar Package Setup"""
import setuptools

from targpg import __version__, __author__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="targpg",
    version=__version__,
    author=__author__,
    author_email="seanslater@whatno.io",
    description="manage secure archive containing sensative docs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/spslater/targpg",
    license="MIT License",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
        "Topic :: System :: Filesystems",
        "Environment :: Console",
    ],
    keywords="filesystem files secure tar gpg",
    python_requires=">=3.6",
)
