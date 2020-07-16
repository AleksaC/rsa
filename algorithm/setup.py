from rsa import __version__
from setuptools import setup

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="rsa",
    version=__version__,
    author="Aleksa Ćuković",
    author_email="aleksacukovic1@gmail.com",
    description="RSA algorithm implementation",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/AleksaC/rsa",
    license="MIT",
    python_requires=">=3.6.1",
    packages=["rsa"],
    entry_points={"console_scripts": ["rsa = rsa.cli:main"]},
)
