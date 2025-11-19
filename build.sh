#!/bin/bash
rm -rf dist/ &&
rm -rf adestis_netbox_applications.egg-info/ &&
rm -rf build/
python3 setup.py sdist bdist_wheel && 
python3 -m twine upload dist/* &&
rm -rf dist/ &&
rm -rf adestis_netbox_applications.egg-info/ &&
rm -rf build/
