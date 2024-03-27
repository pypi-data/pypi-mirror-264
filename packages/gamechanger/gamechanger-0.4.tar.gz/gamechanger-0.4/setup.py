# setup.py

from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    description = f.read()

setup(
    name="gamechanger",
    version="0.4",
    packages=find_packages(),
    install_packages=[],
    author="Abdellatif BELMADY",
    author_email="abdellatif.belmady@gmail.com",
    description="A sample gamechanger library for gamification",
    url="https://github.com/abdellatif-belmady/gamechanger",
    long_description=description,
    long_description_content_type="text/markdown",
)