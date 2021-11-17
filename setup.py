"""Setup.py file
"""
from setuptools import find_packages
from setuptools import setup


with open("version", "r") as f:
    version = f.read()
desc = "Generate an ASCII Art from keyword put in the cli"
url = "https://github.com/Nathanlauga/ascii-art-generator-cli"

setup(
    name="ascii_art",
    version=version,
    description=desc,
    author="Nathan LAUGA",
    author_email="nathan.lauga@protonmail.com",
    url=url,
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "ascii-generator = ascii_art.cmd:ascii_generator",
        ],
    },
)
