from setuptools import setup, find_packages

VERSION = "0.1.0"
DESCRIPTION = "A CLI tool that masks the characters of a website or mobile application"

with open("README.md", "r", encoding="UTF-8") as file:
    README = file.read()


setup(
    name="mask-translate",
    version=VERSION,
    url="https://github.com/benoapp/mask-translate",
    author="Hamze Shekh Najeeb",
    author_email="hamze.najeeb03@gmail.com",
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    entry_points={"console_scripts": ["mask-translate = masktranslate.main:main"]},
)