from setuptools import setup, find_packages

setup(
    name="katodb",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "niconico.py",
        "tqdm",
        "pytube"
    ]
)