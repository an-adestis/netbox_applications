from setuptools import find_packages, setup
from pathlib import Path

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='adestis-netbox-applications',
    version='1.0.18',
    description='ADESTIS Application Management',
    url='https://github.com/an-adestis/netbox_applications',
    author='ADESTIS GmbH',
    author_email='pypi@adestis.de',
    install_requires=['adestis_netbox_certificate_management'],
    packages=find_packages(),
    include_package_data=True,
    license='GPL-3.0-only',
    keywords=['netbox', 'netbox-plugin', 'plugin'],
    package_data={
        "adestis_netbox_applications": ["**/*.html"],
        '': ['LICENSE'],
        
        
    },
    long_description=description,
    long_description_content_type="text/markdown",
)