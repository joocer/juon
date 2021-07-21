from setuptools import setup, find_packages  # type:ignore

with open("juon/version.py", "r") as v:
    vers = v.read()
exec(vers)  # nosec

with open("README.md", "r") as rm:
    long_description = rm.read()

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="juon",
    version=__version__,
    description="Python Graph Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    maintainer="Joocer",
    author="joocer",
    author_email="justin.joyce@joocer.com",
    packages=find_packages(include=["juon", "juon.*"]),
    url="https://github.com/joocer/juon",
    install_requires=required,
)