from setuptools import setup, find_packages

# THIS file is necessary to build the library properly so that pyinstaller can see all methods associated with the code

setup(
    name='connect4app',
    version='2.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'connect4app=connect4app.__main__:main',
        ],
    },
)