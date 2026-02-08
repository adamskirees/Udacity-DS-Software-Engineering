from setuptools import setup, find_packages

setup(
    name="employee_events",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
    ],
    author="Adam Rees",
    description="A package for monitoring employee performance and flight risk based on event data.",
)