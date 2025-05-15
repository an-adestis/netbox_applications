from setuptools import find_packages, setup
from pathlib import Path

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='adestis-netbox-applications',
    version='1.0.6',
    description='ADESTIS Application Management',
    # url='https://github.com/adestis/netbox-account-management',
    author='ADESTIS GmbH',
    author_email='pypi@adestis.de',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    keywords=['netbox', 'netbox-plugin', 'plugin'],
    package_data={
        "adestis_netbox_applications": ["**/*.html"],
        '': ['LICENSE'],
        
        
    },
    long_description=description,
    long_description_content_type="text/markdown",
)