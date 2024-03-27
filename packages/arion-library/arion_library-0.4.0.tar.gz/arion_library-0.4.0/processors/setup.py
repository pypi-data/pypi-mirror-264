from setuptools import setup, find_packages
import os

# Read the version from the environment variable
version = os.environ["VERSION"]

setup(
    name='arion_library',  # Replace with your package name
    version=version,  # Replace with your package version
    author='Heni Nechi',  # Replace with your name
    author_email='h.nechi@arion-tech.com',  # Replace with your email
    url='https://github.com/HaniNechi/arion_library',  # Replace with your repository URL
    packages=find_packages(),  # Automatically find all packages
    python_requires='>=3.8',  # Specify Python version requirements
    install_requires=[
        'pyodbc',
        'pytest',
        'azure-core'
        'azure-data-tables'
        'azure-storage-blob'
        'python-dotenv'
        'pytest'
    ],
)
