from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

NAME = 'fromto'
VERSION = '1.0.0'
DESCRIPTION = 'Package for performing translation operations between Karakalpak and other 204 languages through the from-to.uz site'

# Setting up
setup(
    name=NAME,
    version=VERSION,
    author="Turdıbek Jumabaev",
    author_email="<turdibekjumabaev05@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['karakalpak', 'fromto', 'translator'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
