from setuptools import setup, find_packages

# THIS file is necessary to build the library properly so that pyinstaller can see all methods associated with the code

setup(
    name='connect4',
    version='1.0.0',
    packages=find_packages(),
    scripts=['app/__main__.py'],
)