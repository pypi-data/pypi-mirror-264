from setuptools import setup , find_packages
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name = "TESTING_C_SDK",
    version = "0.0.5",
    packages=find_packages(include=["TESTING_C_SDK.__init__.py"],exclude=['TESTING_C_SDK.egg-info/','TESTING_C_SDK.data_load','TESTING_C_SDK.cglense' ]),
    install_requires = required,

    )