from setuptools import find_packages, setup

setup(
    name='adestis-netbox-applications',
    version='1.0.2',
    description='ADESTIS Applications',
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
    }
)