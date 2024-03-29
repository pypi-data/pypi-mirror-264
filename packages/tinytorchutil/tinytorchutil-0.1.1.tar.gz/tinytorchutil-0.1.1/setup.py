from setuptools import setup, find_packages

setup(
    name='tinytorchutil',
    version='0.1.1',
    packages=find_packages(),
    description='A personal collection of small utility functions for PyTorch.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Chainathan',
    install_requires=[
    'torch',
    'matplotlib',
    'numpy',
    'fastcore',
    'fastprogress',
    'torcheval',
    ],
    python_requires='>=3.6',
)
