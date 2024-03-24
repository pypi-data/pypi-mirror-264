from setuptools import setup, find_packages

setup(
    name='kotsareservation',
    version='0.1.0',
    packages=find_packages(include=['PythonWorkspace', 'PythonWorkspace.*'])
)