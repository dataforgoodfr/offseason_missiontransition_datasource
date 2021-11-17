"""Setup.py file
"""
from setuptools import find_packages
from setuptools import setup


with open("version", "r") as f:
    version = f.read()

desc = "datasource package for mission transition"
url = "https://github.com/dataforgoodfr/offseason_missiontransition_datasource"

setup(
    name="datasource",
    version=version,
    description=desc,
    author="Mission Transition",
    url=url,
    packages=find_packages(),
)
