from unittest import mock

import pytest

from pymoof.util import bleak_utils


@pytest.fixture
def bleak_client(services):
    mock_client = mock.AsyncMock()
    mock_client.get_services.return_value = services
    return mock_client


@pytest.fixture
def uuid():
    return mock.Mock()


@pytest.fixture
def services(service):
    services = mock.Mock()
    services.get_service.return_value = service
    return services


@pytest.fixture
def service(characteristic):
    service = mock.Mock()
    service.get_characteristic.return_value = characteristic
    return service


@pytest.fixture
def characteristic():
    return mock.sentinel.Characteristic


@pytest.mark.asyncio
async def test_get_characteristic(
    bleak_client,
    uuid,
    services,
    service,
    characteristic,
):
    bleak_client.get_services.return_value = services
    result = await bleak_utils.get_characteristic(bleak_client, uuid)
    assert result == characteristic
    service.get_characteristic.assert_called_once_with(
        uuid.value,
    )


@pytest.mark.asyncio
async def test_write_to_characteristic(bleak_client, uuid, characteristic, service):
    data = b"deadbeef"
    await bleak_utils.write_to_characteristic(bleak_client, uuid, data)
    bleak_client.write_gatt_char.assert_called_once_with(
        characteristic,
        data,
        response=True,
    )


@pytest.mark.asyncio
async def test_read_from_characteristic(bleak_client, uuid, characteristic):
    data = b"deadbeef"
    bleak_client.read_gatt_char.return_value = data

    result = await bleak_utils.read_from_characteristic(bleak_client, uuid)
    assert result == data

    bleak_client.read_gatt_char.assert_called_once_with(characteristic)
