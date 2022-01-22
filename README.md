# pymoof
Exploring bluetooth functionality of the Vanmoof SX3

## Usage
```python
from pymoof.clients.sx3 import SX3Client

client = SX3Client(bleak_client, encryption_key)
client.authenticate()
```
You must have an instantiated bleak client that is connected to the bike. See `pymoof/tools/discover_bike.py` to determine which device is your bike and `pymoof/tools/retrieve_encryption_key.py` to connect to Vanmoof servers to get your encryption key.

See `example.py` for more info on useage.
