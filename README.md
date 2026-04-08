# Netbox Application Plugin

The **NetBox Application Plugin** extends NetBox with the ability to manage applications and link them to various existing NetBox objects.

## Features

- Manage applications directly within NetBox
- Flexible association of applications with existing NetBox objects

This plugin provide following Models:
- Application
- Software
- Application Type


## Screenshots

![Applications Details](https://github.com/an-adestis/netbox_applications/blob/92b2ea248759877e923063c1a18628832442371f/applications01.png)

![Applications View](https://github.com/an-adestis/netbox_applications/blob/92b2ea248759877e923063c1a18628832442371f/applications02.png)

![Software Details](https://github.com/an-adestis/netbox_applications/blob/92b2ea248759877e923063c1a18628832442371f/software01.png)

![Software View](https://github.com/an-adestis/netbox_applications/blob/92b2ea248759877e923063c1a18628832442371f/software02.png)

## Compatibility

> **Note**: This plugin depends on the [`adestis-netbox-certificate-management`](https://pypi.org/project/adestis-netbox-certificate-management/) plugin.  
> Therefore, its compatibility is directly tied to the NetBox version used in the base image.

The plugin is developed and tested using the following base image:

```dockerfile
ARG FROM_TAG=v4.3.7-3.3.0  # NetBox v4.3.7
```

## Installation

The plugin is available on PyPI and can be installed via pip:

```bash
pip install adestis-netbox-applications
```
