from setuptools import setup, find_packages

setup(
    name="calculator",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pytest>=8.4.0",
        "requests>=2.32.4",
        "urllib3>=2.4.0",
    ],
)