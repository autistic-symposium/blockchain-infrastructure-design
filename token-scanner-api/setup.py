from setuptools import setup, find_packages

setup(
    name="indexer",
    version='0.0.3',
    packages=find_packages(include=[
        'src', 
        'src.blockchains', 
        'src.server', 
        'src.utils']),
    author="steinkirch.eth",
    install_requires=['python-dotenv'],
    entry_points={
        'console_scripts': ['indexer=src.main:run']
    },
)