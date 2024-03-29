from setuptools import find_packages
from setuptools import setup

with open("anson/version.py", "r") as v:
    vers = v.read()
exec(vers)  # nosec

with open("README.md", "r") as rm:
    long_description = rm.read()

try:
    with open("requirements.txt", "r") as f:
        required = f.read().splitlines()
except:
    with open("anson.egg-info/requires.txt", "r") as f:
        required = f.read().splitlines()

setup(
    name="anson",
    version=__version__,
    description="Columnar Data Format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    maintainer="Joocer",
    author="joocer",
    author_email="justin.joyce@joocer.com",
    packages=find_packages(include=["anson", "anson.*"]),
    url="https://github.com/mabel-dev/anson/",
    install_requires=required,
)
