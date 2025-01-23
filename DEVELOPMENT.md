# Development Instructions

## Table of contents

- [Development Instructions](#development-instructions)
  - [Table of contents](#table-of-contents)
  - [Required software](#required-software)
  - [Get ready](#get-ready)
    - [How to setup the development environment](#how-to-setup-the-development-environment)
    - [How can I start the development environment?](#how-can-i-start-the-development-environment)
  - [Release on pypi](#release-on-pypi)
  - [FAQ](#faq)
    - [Where could I find the credentials for X?](#where-could-i-find-the-credentials-for-x)
    - [Should I restart the entire services if I would like to see the changes on my local machine?](#should-i-restart-the-entire-services-if-i-would-like-to-see-the-changes-on-my-local-machine)
    - [Some packages are available on my local machine. I do not know how to use methods and classes of netbox.](#some-packages-are-available-on-my-local-machine-i-do-not-know-how-to-use-methods-and-classes-of-netbox)
    - [How can I create new database migrations?](#how-can-i-create-new-database-migrations)


## Required software

-  Python 3.11
-  VS Code
-  Docker

## Get ready

### How to setup the development environment

1. Install pip: `python -m pip install --user --upgrade pip`
2. Create a virtual environment
   1. The virtual environment is used to save your dependencies for this project
   2. Open the powershell and execute `python -m venv venv` in the root folder
   3. Active your environment in powershell with `.\venv\Scripts\Activate.ps1` (you need to start this script everytime)
   4. Execute `pip install -r .\dev\dev-requirements.txt`
3. Install python extensions for VS Code

### How can I start the development environment?

1. Go to the docker folder
2. execute `docker compose up --build`


## Release on pypi

1. Increase the version numbers

2. Go to the root folder and execute

```bash
python setup.py sdist bdist_wheel && 
python -m twine upload dist/* &&
rm -rf dist/ &&
rm -rf adestis_netbox_applications.egg-info/ &&
rm -rf build/
```

## FAQ

### Where could I find the credentials for X?
Just view the docker-compose files or check the files in ``docker/env`

### Should I restart the entire services if I would like to see the changes on my local machine?

No. You must execute `docker compose up --build netbox`

### Some packages are available on my local machine. I do not know how to use methods and classes of netbox.

Netbox did not release a python package yet. In order to to see the implementation netbox resources you must download the netbox project on github and open it in your IDE.

### How can I create new database migrations?

You need to mount the local storage to a path on the container.
Afterwards you must open a shell on the container and execute `python manage.py makemigrations adestis_netbox_applications`.
