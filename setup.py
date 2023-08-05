from setuptools import setup, find_packages

def _requires_from_file(filename):
    return open(filename).read().splitlines()

setup(
    name="katodb",
    version="0.0.1",
    packages=find_packages(),
    install_requires=_requires_from_file("requirements.txt"),
    python_requires="==3.9",
)