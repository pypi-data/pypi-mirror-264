from setuptools import setup, find_packages
from mehrcalculator.mehrcalculator import Calculator

setup(
    name='calculator_package',
    version='0.2',
    packages=find_packages(),
    install_requires=[],  # Any dependencies
    author='Ramin Baghaei Mehr',
    author_email='ramin.mehr@gmail.com',
    description='A simple calculator package.'
)
