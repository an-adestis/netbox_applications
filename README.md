# Netbox Application Plugin

Netbox Plugin for Application related objects documentation.
## Features

This plugin provide following Model:
* Applications

## Compatibility

|               |           |
|---------------|-----------|
| NetBox 3.4.x  | >= 0.9.0  |


## Installation

The plugin is available as a Python package in pypi and can be installed with pip  

```
pip install adestis_netbox_applications
```
Enable the plugin in /etc/netbox/config/configuration.py:
```
PLUGINS = ['adestis_netbox_applications']
```
Restart NetBox and add `adestis_netbox_applications` to your local_requirements.txt

See [NetBox Documentation](https://docs.netbox.dev/en/stable/plugins/#installing-plugins) for details


## Screenshots

Applications
![Add](./docs/Images/image.png)

Applications
![Results](./docs/Images/image-1.png)