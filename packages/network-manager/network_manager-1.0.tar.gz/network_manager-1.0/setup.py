from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0'
DESCRIPTION = 'Network Manager for Activating and Deactivating Features on Network Devices'
LONG_DESCRIPTION = """
A package that allows for managing network devices by activating and deactivating certain features such as firewall settings and parental controls.

Features:
- Activating firewall settings
- Deactivating firewall settings
- Activating parental controls
- Deactivating parental controls
"""

# Setting up
setup(
    name="network_manager",
    version=VERSION,
    author="Your Name",
    author_email="<your.email@example.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['selenium'],  # Add any other dependencies here
    keywords=['python', 'network', 'device', 'firewall', 'parental control', 'selenium'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
