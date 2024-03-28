from setuptools import setup, find_packages
import codecs
import os
import urllib.request

#Get this dir
here = os.path.abspath(os.path.dirname(__file__))

#Download readme file from github repo
urllib.request.urlretrieve("https://github.com/aidens113/simpleSeleniumWrapper/raw/main/README.md", filename=f"{here}/README.md")

#Read readme.md file for setup
with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()#.split('---')[2]

version = '0.3.4'
description = 'An easy-to-use wrapper for Selenium in Python. This package is intended to make writing web automation software in Python as painless as possible!'

# Setting up 
setup(
    name="simpleseleniumwrapper",
    version=version,
    author="Aiden S",
    author_email="<admin@data-alchemy.net>",
    description=description,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['selenium>=4.0'],
    keywords=['python', 'selenium', 'automation', 'wrapper', 'chromedriver','geckodriver','undetected','webdriver','manager'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Topic :: System :: Operating System Kernels :: Linux",
        "Operating System :: Microsoft :: Windows",
    ]
)
