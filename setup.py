from setuptools import setup, find_packages  # type:ignore

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    required = f.read().splitlines()

with open("diablo/version.py", "r") as v:
    vers = v.read()
exec(vers)  # nosec

setup(
    name="diablo",
    version=__version__,
    description="Python Graph Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="joocer",
    author_email="justin.joyce@joocer.com",
    packages=find_packages('diablo'),
    url="https://github.com/joocer/diablo",
    install_requires=required,
)