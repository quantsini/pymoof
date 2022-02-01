from unittest import mock

import pytest

from pymoof.clients.sx3 import BellTone
from pymoof.clients.sx3 import SX3Client


@pytest.fixture
def key():
    return "a" * 32


@pytest.fixture
def bleak_client(services):
    mock_client = mock.AsyncMock()
    mock_client.get_services.return_value = services
    return mock_client


@pytest.fixture
def services(service):
    services = mock.Mock()
    services.get_service.return_value = service
    return services


@pytest.fixture
def service():
    return mock.Mock()


@pytest.fixture
def client(bleak_client, key):
    return SX3Client(bleak_client, key)


@pytest.mark.asyncio
async def test_authenticate(bleak_client, client, services, service):
    bleak_client.read_gatt_char.return_value = b"ab"
    await client.authenticate()


@pytest.mark.asyncio
async def test_set_bell_tone(bleak_client, client):
    bleak_client.read_gatt_char.return_value = b"ab"
    await client.set_bell_tone(BellTone.PARTY)
