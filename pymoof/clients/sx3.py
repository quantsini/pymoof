from enum import Enum

import bleak.backends.client

from pymoof.profiles.sx3 import SX3Profile
from pymoof.util import bleak_utils


class BellTone(Enum):

    BOAT = 0x18
    PARTY = 0x17
    BELL = 0x16


class LockState(Enum):

    UNLOCKED = 0x00
    LOCK = 0x01
    ATTEMPT_UNLOCK = 0x02


class SX3Client:
    """Collection of functions to interact with a Vanmoof SX3 over bluetooth"""

    def __init__(
        self,
        bleak_client: bleak.backends.client.BaseBleakClient,
        key: str,
    ) -> None:
        self._gatt_client = bleak_client
        self._bike_profile = SX3Profile(key)

    async def _get_nonce(self) -> bytes:
        return await self._read(
            self._bike_profile.Security.CHALLENGE,
            needs_decryption=False,
        )

    async def _read(self, characteristic_uuid, needs_decryption: bool = True) -> bytes:
        result = await bleak_utils.read_from_characteristic(
            self._gatt_client,
            characteristic_uuid,
        )

        if needs_decryption:
            result = self._bike_profile.decrypt_payload(result)

        return result

    async def _write(self, characteristic_uuid, data: bytes) -> None:
        nonce = await self._get_nonce()
        payload = self._bike_profile.build_encrypted_payload(nonce, data)

        await bleak_utils.write_to_characteristic(
            self._gatt_client,
            characteristic_uuid,
            payload,
        )

    # XXX: Maybe pull the profile specific uuids out into the profiles themselves?
    async def authenticate(self) -> None:
        nonce = await self._get_nonce()
        payload = self._bike_profile.build_authentication_payload(nonce)

        await bleak_utils.write_to_characteristic(
            self._gatt_client,
            self._bike_profile.Security.KEY_INDEX,
            payload,
        )

    async def set_bell_tone(self, bell_tone: BellTone) -> None:
        await self._write(
            self._bike_profile.Sound.BELL_SOUND,
            [bell_tone.value],
        )

    async def set_lock_state(self, state: LockState) -> None:
        await self._write(
            self._bike_profile.Defense.LOCK_STATE,
            [state.value],
        )

    async def set_power_level(self, level: int) -> None:
        assert 0 <= level <= 5

        await self._write(
            self._bike_profile.Movement.POWER_LEVEL,
            [level, 0x1],
        )

    async def get_battery_level(self) -> int:
        result = await self._read(
            self._bike_profile.BikeInfo.MOTOR_BATTERY_LEVEL,
        )

        return int(result[0])

    async def get_lock_state(self) -> LockState:
        result = await self._read(
            self._bike_profile.Defense.LOCK_STATE,
        )

        return LockState(result[0])

    async def get_distance_travelled(self) -> float:
        # Returns kilometers, stored as hectometers
        result = await self._read(
            self._bike_profile.Movement.DISTANCE,
        )
        return int.from_bytes(result, "little") / 10

    async def get_power_level(self) -> int:
        result = await self._read(
            self._bike_profile.Movement.POWER_LEVEL,
        )

        return result[0]

    async def get_frame_number(self) -> str:
        result = await self._read(
            self._bike_profile.BikeInfo.FRAME_NUMBER,
            needs_decryption=False,
        )

        return result.decode("ascii")

    async def get_sound_volume(self) -> bytes:
        result = await self._read(
            self._bike_profile.Sound.SOUND_VOLUME,
        )

        # TODO: parse this
        return result

    async def get_speed(self) -> bytes:
        result = await self._read(
            self._bike_profile.Movement.SPEED,
        )

        # TODO: parse this
        return result
