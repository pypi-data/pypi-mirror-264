from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
import subprocess
import os


with open('README.md') as f:
    long_description = f.read()

setup(
    name='threed_optix',
    version='4.2.6',
    license='MIT',
    author="3DOptix",
    author_email='ereztep@3doptix.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://3doptix.com',
    keywords=["Optics", "Optical Design", "Optical Simulation", "Optical Design Software", "3DOptix"],
    install_requires=[
        'requests',
        'pandas',
        'matplotlib',
        'plotly',
        'colorama',
        'nbformat',
        'numpy',
        'scikit-image',
        'scipy',
        'opencv-python',
        'dill',
        "ply",
        "networkx",
        "pytest",
        #'matlab2python @ git+https://github.com/ebranlard/matlab2python.git#egg=matlab2python',
    ],
)
