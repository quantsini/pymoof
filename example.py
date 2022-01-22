import asyncio

import bleak

from pymoof.clients.sx3 import SX3Client
from pymoof.tools import discover_bike
from pymoof.tools import retrieve_encryption_key


async def example():
    print("Getting key from vanmoof servers")
    key = retrieve_encryption_key.query()

    print("Discovering nearby vanmoof bikes")
    address = await discover_bike.query()

    print("Doing example commands")
    async with bleak.BleakClient(address) as bleak_client:
        client = SX3Client(bleak_client, key)

        print("Frame Number:", await client.get_frame_number())

        await client.authenticate()

        # await client.set_bell_tone(BellTone.BELL)
        print("Battery Level:", await client.get_battery_level(), "%")
        # await client.set_lock_state(LockState.UNLOCKED)
        print("Distance Travelled:", await client.get_distance_travelled(), "km")
        # await client.set_power_level(2)
        print("Power level:", await client.get_power_level())
        print("Sound Volume:", await client.get_sound_volume())
        print("Lock State:", await client.get_lock_state())


asyncio.run(example())
