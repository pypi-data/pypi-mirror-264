# Project Title

YAML substitution

## Project Shields

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Supported Python Versions][img_pyversions]][url_pyversions]
[![PyPI Releases][img_pypi]][url_pypi]

[img_pyversions]: https://img.shields.io/pypi/pyversions/yamlsub.svg
[url_pyversions]: https://pypi.python.org/pypi/yamlsub
[img_pypi]: https://img.shields.io/badge/PyPI-wheels-green.svg
[url_pypi]: https://pypi.org/project/yamlsub/#files

## Table of Contents

- [Project Title](#project-title)
  - [Project Shields](#project-shields)
  - [Table of Contents](#table-of-contents)
  - [About ](#about-)
  - [Getting Started ](#getting-started-)
    - [Prerequisites](#prerequisites)
    - [Installing](#installing)
  - [Usage ](#usage-)

## About <a name = "about"></a>

A wrapper around the [dotenv](https://pypi.org/project/dotenv/) and [pyaml-env](https://pypi.org/project/pyaml-env/) packages.

## Getting Started <a name = "getting_started"></a>

This project just serves as a wrapper to load environment variables from a .env file, and then update a YAML configuration file with environment variables as needed / required.

It's important to view the documentation for the [pyaml-env](https://pypi.org/project/pyaml-env/) and [dotenv](https://pypi.org/project/dotenv/) projects.

### Prerequisites

* python, version 3.11+
* python's [build package](https://pypi.org/project/build/): ```pip install build```

### Installing

To install using pip:
```
pip install yamlsub
```

To include the package from VCS in a project, you can follow the [pip documentation](https://pip.pypa.io/en/latest/topics/vcs-support/#vcs-support) to import a GitHub project.

For example:
```
pip install yamlsub@git+https://github.com/willmorejg/yamlsub.git
```

## Usage <a name = "usage"></a>
Review the documentation for the [pyaml-env](https://pypi.org/project/pyaml-env/) and [dotenv](https://pypi.org/project/dotenv/) projects for additioanl information on how best to incorporate this project into other projects.

Using an example .env file containing the following ...
```
DB_HOST=localhost
DB_USER=root
DB_PASS=123456
```
... and a sample config.yaml file ...
```
database:
  host: !ENV ${DB_HOST}
  user: !ENV ${DB_USER}
  pass: !ENV ${DB_PASS}
```
... and the following code ...

```
from yamlsub.config import Config

cfg = Config(env_path='.env', yaml_path='config.yaml')

```
, you can access configuration values as follows:
```
database_config = cfg.get_config_key('database')
dbhost = database_config['host']
dbuser = database_config['user']
dbpass = database_config['pass']

print(f'Host: {dbhost}, User: {dbuser}, Pass: {dbpass}')
```
