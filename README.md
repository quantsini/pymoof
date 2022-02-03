# pymoof
[![ReadTheDocs](https://readthedocs.org/projects/pymoof/badge/?version=latest)](https://pymoof.readthedocs.io/en/latest/) [![PyPI version](https://badge.fury.io/py/pymoof.svg)](https://badge.fury.io/py/pymoof) [![Tests](https://github.com/quantsini/pymoof/actions/workflows/test.yml/badge.svg)](https://github.com/quantsini/pymoof/actions/workflows/test.yml)

Connect to your Vanmoof S3 and X3 through bluetooth.

## Installation

Install python 3.7+, then use pip to install pymoof.
`pip install pymoof`

## Usage

pymoof was tested to work on MacOS 12.1, Ubuntu 20.04.3 LTS, and a Raspberry Pi 3 b+ running Raspberry Pi OS (32-bit) / 2021-10-30.
```python
from pymoof.clients.sx3 import SX3Client
import bleak

...

device = ...
key = ...

async with bleak.BleakClient(device) as bleak_client:
	client = SX3Client(bleak_client, encryption_key)
	await client.authenticate()
```
You must have an instantiated [bleak](https://bleak.readthedocs.io/en/latest/) client that is connected to the bike. See `pymoof.tools.discover_bike` to determine which device is your bike and `pymoof.tools.retrieve_encryption_key` to connect to Vanmoof servers to get your encryption key.

See `example.py` for additional usage.

## Contributing

Contributions are welcome and encouraged! Every bit helps and credit will be given.

Ways you can help:

### Reporting Bugs

You can report bugs through the github issue tracker: https://github.com/quantsini/pymoof/issues

Useful information to include when reporting bugs:

* Version of pymoof
* The operating system where pymoof was used
* What Vanmoof bike was used
* Detailed steps on reproducing an issue

### Help with reverse engineering

Vanmoof bikes communicate through Bluetooth Low Energy. I've tried my best to get all the BLE GATT UUIDs, however, some reverse engineering is needed to figure out what the payloads represent. I suggest using a packet sniffer like [wireshark](https://www.wireshark.org) to analyze data from the official Vanmoof app and the bike.

### Writing Documentation

Good documentation is always good!

### Getting Started with Development

You want to contribute? Awesome! Here are some steps to get you up and running.
This project uses [Poetry](https://python-poetry.org/docs/master/#installing-with-the-official-installer) for package and dependency management and [tox](https://www.tox.wiki/) for tests.

1. Create a fork of the _pymoof_ github repo.
2. Clone it locally:
```
git clone git@github.com:<your username>/pymoof.git
```
3. Get the [latest version of poetry](https://python-poetry.org), a package and dependency management tool.
4. Install dependencies
```
poetry install
```
5. Activate your shell. This should put you in a virtualenv that allows you to run tests.
```
poetry shell
```
6. You should now be able to run tests and make modifications. You can run tests by running tox under poetry
```
poetry run tox
```
7. Go forth and make great changes!
