# pymoof
Connect to your Vanmoof S3 and X3 through bluetooth.

## Installation
Install python 3.7+, then use pip to install pymoof.
`pip install pymoof`

## Usage
pymoof was tested to work on MacOS 12.1, Ubuntu 20.04.3 LTS, and a Raspberry Pi 3 b+ running Raspberry Pi OS (32-bit) / 2021-10-30.
```python
from pymoof.clients.sx3 import SX3Client

client = SX3Client(bleak_client, encryption_key)
client.authenticate()
```
You must have an instantiated bleak client that is connected to the bike. See `pymoof.tools.discover_bike` to determine which device is your bike and `pymoof.tools.retrieve_encryption_key` to connect to Vanmoof servers to get your encryption key.

See `example.py` for more info on useage.

## Contributing
This project uses [Poetry](https://python-poetry.org/docs/master/#installing-with-the-official-installer) for package and dependency management. It also uses [tox](https://www.tox.wiki/) for test running and pre-commit for running linters.
