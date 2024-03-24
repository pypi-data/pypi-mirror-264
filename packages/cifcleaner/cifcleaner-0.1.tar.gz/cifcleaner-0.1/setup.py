from setuptools import setup, find_packages

setup(
    name='cifcleaner',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'click==8.1.7',
        'gemmi==0.6.5',
        'matplotlib==3.8.3',
        'numpy==1.26.4',
        'pandas==2.2.1',
        'pytest==8.0.1',
    ],
)
