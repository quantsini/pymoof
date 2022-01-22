from unittest import mock

import pytest

from pymoof.clients.sx3 import SX3Client


@pytest.fixture
def key():
    return "a" * 16


@pytest.fixture
def bleak_client():
    return mock.Mock()


@pytest.fixture
def client(bleak_client, key):
    return SX3Client(bleak_client, key)


def test_client(client):
    # TODO
    pass
