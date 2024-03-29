from setuptools import setup, find_packages

setup(
    name='ArtusAPI',
    version='0.1.0',
    description='API to control Artus Family of Robots',
    package_dir={'': 'ArtusAPI'},  # tells setuptools that your packages are under src
    packages=find_packages(where='ArtusAPI'),
    # other setup configurations
)