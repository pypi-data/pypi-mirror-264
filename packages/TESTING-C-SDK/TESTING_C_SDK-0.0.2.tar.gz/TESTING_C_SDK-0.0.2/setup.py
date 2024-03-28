from setuptools import setup , find_packages
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name = "TESTING_C_SDK",
    version = "0.0.2",
    packages=find_packages(),
    install_requires = required,

    )