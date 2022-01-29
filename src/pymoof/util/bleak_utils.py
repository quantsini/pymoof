import bleak.backends.characteristic
import bleak.backends.client


async def get_characteristic(
    gatt_client: bleak.backends.client.BaseBleakClient,
    char_uuid,
) -> bleak.backends.characteristic.BleakGATTCharacteristic:
    services = await gatt_client.get_services()
    service = services.get_service(char_uuid.SERVICE_UUID.value)
    return service.get_characteristic(char_uuid.value)


async def write_to_characteristic(
    gatt_client: bleak.backends.client.BaseBleakClient,
    uuid,
    data: bytes,
) -> None:
    characteristic = await get_characteristic(gatt_client, uuid)
    await gatt_client.write_gatt_char(characteristic, data, response=True)


async def read_from_characteristic(
    gatt_client: bleak.backends.client.BaseBleakClient,
    uuid,
) -> bytes:
    characteristic = await get_characteristic(gatt_client, uuid)
    return await gatt_client.read_gatt_char(characteristic)
