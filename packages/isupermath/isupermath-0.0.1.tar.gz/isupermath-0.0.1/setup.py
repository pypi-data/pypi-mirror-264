from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'isupermath'
LONG_DESCRIPTION = 'A package to perform basic maths'

# Setting up
setup(
    name="isupermath",
    version=VERSION,
    author="Iffiisyed",
    author_email="iffiisyed@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['arithmetic', 'supermath', 'mathematics', 'python tutorial', 'iffiisyed'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)