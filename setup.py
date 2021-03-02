from setuptools import setup, find_packages  # type:ignore

with open("README.md", "r") as fh:
    long_description = fh.read()

version = eval(open("diablo/version.py", "r").read())  # nosec

setup(
    name="diablo",
    version=version,
    description="Python Graph Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="joocer",
    author_email="justin.joyce@joocer.com",
    packages=find_packages('diablo'),
    url="https://github.com/joocer/diablo",
    install_requires=[''],
)