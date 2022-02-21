from unittest import mock

import pytest

from pymoof.clients.sx3 import BellTone
from pymoof.clients.sx3 import LockState
from pymoof.clients.sx3 import Sound
from pymoof.clients.sx3 import SX3Client


@pytest.fixture
def key():
    return "a" * 32


@pytest.fixture
def user_key_id():
    return 1


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
def client(bleak_client, key, user_key_id):
    return SX3Client(bleak_client, key, user_key_id)


@pytest.mark.asyncio
async def test_authenticate(bleak_client, client, services, service):
    bleak_client.read_gatt_char.return_value = b"ab"
    await client.authenticate()


# Smoke tests
@pytest.mark.asyncio
async def test_set_bell_tone(bleak_client, client):
    bleak_client.read_gatt_char.return_value = b"ab"
    await client.set_bell_tone(BellTone.PARTY)


@pytest.mark.asyncio
async def test_set_lock_state(bleak_client, client):
    bleak_client.read_gatt_char.return_value = b"ab"
    await client.set_lock_state(LockState.UNLOCKED)


@pytest.mark.asyncio
async def test_set_power_level(bleak_client, client):
    bleak_client.read_gatt_char.return_value = b"ab"
    await client.set_power_level(0)


@pytest.mark.asyncio
async def test_play_sound(bleak_client, client):
    bleak_client.read_gatt_char.return_value = b"ab"
    await client.play_sound(Sound.SCROLLING_TONE, 1)


@pytest.mark.asyncio
async def test_get_battery_level(bleak_client, client):
    bleak_client.read_gatt_char.return_value = b"a" * 32
    await client.get_battery_level()


@pytest.mark.asyncio
async def test_get_distance_travelled(bleak_client, client):
    bleak_client.read_gatt_char.return_value = b"a" * 32
    await client.get_distance_travelled()


@pytest.mark.asyncio
async def test_get_power_level(bleak_client, client):
    bleak_client.read_gatt_char.return_value = b"a" * 32
    await client.get_power_level()
    await client.get_distance_travelled()


@pytest.mark.asyncio
async def test_frame_number(bleak_client, client):
    bleak_client.read_gatt_char.return_value = b"a" * 32
    await client.get_frame_number()


@pytest.mark.asyncio
async def test_sound_volume(bleak_client, client):
    bleak_client.read_gatt_char.return_value = b"a" * 32
    await client.get_sound_volume()


@pytest.mark.asyncio
async def test_get_speed(bleak_client, client):
    bleak_client.read_gatt_char.return_value = b"a" * 32
    await client.get_speed()
