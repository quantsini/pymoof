from unittest import mock

import pytest

from pymoof.clients.sx3 import SX3Client


@pytest.fixture
def key():
    return "a" * 32


@pytest.fixture
def bleak_client():
    return mock.Mock()


@pytest.fixture
def client(bleak_client, key):
    return SX3Client(bleak_client, key)


@pytest.mark.asyncio
async def test_client(client):
    pass
