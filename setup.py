# setup.py
# Copyright 2011 Roger Marsh
# Licence: See LICENCE (BSD licence)
"""solentware-misc setup file."""

from setuptools import setup

if __name__ == "__main__":

    long_description = open("README").read()

    setup(
        name="solentware-misc",
        version="1.3.1",
        description="Classes perhaps useful beyond original application",
        author="Roger Marsh",
        author_email="roger.marsh@solentware.co.uk",
        url="http://www.solentware.co.uk",
        packages=[
            "solentware_misc",
            "solentware_misc.core",
            "solentware_misc.gui",
            "solentware_misc.workarounds",
        ],
        long_description=long_description,
        license="BSD",
        classifiers=[
            "License :: OSI Approved :: BSD License",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Operating System :: OS Independent",
            "Topic :: Software Development",
            "Intended Audience :: Developers",
            "Development Status :: 3 - Alpha",
        ],
    )
