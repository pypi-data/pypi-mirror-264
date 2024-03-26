from setuptools import setup, find_packages

VERSION = "1.0.2"

f = open("README.md", "r")
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name="sievedata",
    version=VERSION,
    description="Sieve CLI and Python Client",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Sieve Team",
    author_email="developer@sievedata.com",
    url="https://github.com/sieve-data/sieve",
    license="unlicensed",
    packages=find_packages(exclude=["ez_setup", "tests*"]),
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.0",
        "click>=8.0",
        "pydantic>=2.0",
        "pathlib>=1.0.1",
        "tqdm==4.64.1",
        "networkx",
        "typeguard",
        "pillow",
        "typer>=0.7.0",
        "rich",
        "cloudpickle",
        "docstring_parser",
        "jsonref",
        "protobuf>=3.20.0,<=3.20.3",
        "pyyaml",
        "grpcio==1.60.0",
        "sseclient",
        "python-dateutil",
    ],
    entry_points={
        "console_scripts": [
            "sieve = sieve._cli.sieve:start_cli",
        ]
    },
)
