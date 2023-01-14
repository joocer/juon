# python setup.py build_ext --inplace

from setuptools import setup, find_packages  # type:ignore
from Cython.Build import cythonize

with open("seren/version.py", "r") as v:
    vers = v.read()
exec(vers)  # nosec

with open("README.md", "r") as rm:
    long_description = rm.read()

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="seren",
    version=__version__,
    description="Python Graph Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    maintainer="Joocer",
    author="joocer",
    author_email="justin.joyce@joocer.com",
    packages=find_packages(include=["seren", "seren.*"]),
    url="https://github.com/joocer/seren",
    install_requires=required,
    ext_modules=cythonize(
        [
            "seren/graphs/common.py",
            "seren/graphs/graph_traversal.py",
            "seren/graphs/graph.py",
            "seren/graphs/internals.py",
        ]
    ),
)
