import os

from setuptools import find_packages, setup


def read_requirements(req_path: str = "requirements.txt"):
    if not os.path.exists(req_path):
        return []

    with open(req_path, "r") as req:
        return [line.strip() for line in req if line.strip()]


setup(
    name="securityriskcard",
    version="0.0.2",
    packages=find_packages(),
    install_requires=read_requirements(),
    tests_require=read_requirements("requirements-test.txt"),
)
