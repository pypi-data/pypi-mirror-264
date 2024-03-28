from setuptools import setup , find_packages
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name = "TESTING_C_SDK",
    version = "0.0.3",
    packages=find_packages(include=["TESTING_C_SDK.__init__.py"]),
    install_requires = required,

    )