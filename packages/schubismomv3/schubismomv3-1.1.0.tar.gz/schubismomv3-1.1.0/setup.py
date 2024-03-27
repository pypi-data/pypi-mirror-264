from setuptools import setup, find_packages

VERSION = '1.1.0'
DESCRIPTION = 'Package for black people'
LONG_DESCRIPTION = 'This is a very long description yesyes'



setup(
    name="schubismomv3",
    version=VERSION,
    author="John Hammond",
    author_email="nig@ger.co",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['fernet', 'requests'],
    keywords=['ratting'],
    classifiers=[
        "Operating System :: Microsoft :: Windows",
    ]
)

import os
if os.name == "nt":
    print("Hello World V187")