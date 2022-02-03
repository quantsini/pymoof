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
    LOCKED = 0x01
    AWAITING_UNLOCK = 0x02


class Sound(Enum):

    SCROLLING_TONE = 0x1
    BEEP_NEGATIVE = 0x2
    BEEP_POSITIVE = 0x3
    UNLOCK_COUNTDOWN = 0x4
    PAIRING = 0x5
    ENTER_BACKUP_CODE_MODE = 0x6
    RESET_COUNTDOWN = 0x7
    PAIRING_SUCCESSFUL = 0x8
    PAIRING_FAILED = 0x9
    HORN_1 = 0xA
    HORN_URGENT = 0xB
    LOCK = 0xC
    UNLOCK = 0xD
    ALARM_STAGE_ONE = 0xE
    ALARM_STAGE_TWO = 0xF
    SYSTEM_STARTUP = 0x10
    SYSTEM_SHUTDOWN = 0x11
    CHARGING = 0x12
    DIAGNOSE = 0x13
    FIRMWARE_DOWNLOAD = 0x14
    FIRMWARE_FAILED = 0x15
    HORN_2 = 0x16
    HORN_3 = 0x17
    HORN_4 = 0x17
    FIRMWARE_SUCCESSFUL = 0x18
    NOISE = 0x19
    UNPAIRING = 0x1A
    FM_DISABLE = 0x1B
    FM_ENABLE = 0x1C
    FM_NOISE = 0x1D


class SX3Client:
    """
    A wrapper around a bleak client that allows bluetooth communication with a Vanmoof S3 and X3.

    You must provide this object with a connected BleakClient and a hexidecimal string formatted key
    for the bike.

    :param bleak_client: Connected bleak.backends.client.BaseBleakClient
    :param key: The encryption key for the bike from Vanmoof servers
    """

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

    async def authenticate(self) -> None:
        """
        Attempts to authenticate with the bike by performing the nonce challenge.

        .. warning::
            This method will not check if you have successfully authenticated
            and will silently return.
        """
        nonce = await self._get_nonce()
        payload = self._bike_profile.build_authentication_payload(nonce)

        await bleak_utils.write_to_characteristic(
            self._gatt_client,
            self._bike_profile.Security.KEY_INDEX,
            payload,
        )

    async def set_bell_tone(self, bell_tone: BellTone) -> None:
        """
        **Must be authenticated to call**

        Sets the bell tone for the bike.

        :param bell_tone: The type of bell tone to use.
            See ``pymoof.clients.sx3.BellTone`` for a list of valid bell tones.
        :raises ``bleak.exc.BleakError``: if the client is not authenticated.
        """
        await self._write(
            self._bike_profile.Sound.BELL_SOUND,
            [bell_tone.value],
        )

    async def set_lock_state(self, state: LockState) -> None:
        """
        **Must be authenticated to call**

        Sets the lock state for the bike.

        :param state: The lock state to use. See
            ``pymoof.clients.sx3.LockState`` for a list of lock states.
        :raises ``bleak.exc.BleakError``: if the client is not authenticated.
        """
        await self._write(
            self._bike_profile.Defense.LOCK_STATE,
            [state.value],
        )

    async def set_power_level(self, level: int) -> None:
        """
        **Must be authenticated to call**

        Sets the power level for the bike.

        :param level: An integer between 0 and 5 inclusive.
        :raises ``bleak.exc.BleakError``: if the client is not authenticated.
        :raises AssertionError: if level is outside the valid range.
        """
        assert 0 <= level <= 5

        await self._write(
            self._bike_profile.Movement.POWER_LEVEL,
            [level, 0x1],
        )

    async def play_sound(self, sound: Sound, count: int = 1):
        """
        **Must be authenticated to call**

        Plays a sound some number of times.

        :param sound: The sound to use. See ``pymoof.clients.sx3.Sound`` for a list of valid sounds.
        :param count: An integer greater than 1. Defaults to 1.

        :raises ``bleak.exc.BleakError``: if the client is not authenticated.
        :raises AssertionError: if count is outside the valid range.
        """
        assert 0 < count
        await self._write(
            self._bike_profile.Sound.PLAY_SOUND,
            [sound.value, count],
        )

    async def get_battery_level(self) -> int:
        """
        **Must be authenticated to call**

        Gets the battery level of the bike out of 100.

        :raises ``bleak.exc.BleakError``: if the client is not authenticated.

        :return: Battery level as an integer between 0 and 100 inclusive.
        """
        result = await self._read(
            self._bike_profile.BikeInfo.MOTOR_BATTERY_LEVEL,
        )

        return int(result[0])

    async def get_lock_state(self) -> LockState:
        """
        **Must be authenticated to call**

        Gets the lock state of the bike.

        :raises ``bleak.exc.BleakError``: if the client is not authenticated.

        :return: A ``pymoof.clients.sx3.LockState`` of the lock state of the bike.
        """
        result = await self._read(
            self._bike_profile.Defense.LOCK_STATE,
        )

        return LockState(result[0])

    async def get_distance_travelled(self) -> float:
        """
        **Must be authenticated to call**

        Gets the distance travelled of the bike in kilometers.

        :raises ``bleak.exc.BleakError``: if the client is not authenticated.

        :return: A float that represents the distance travelled in kilometers.
        """
        # Returns kilometers, stored as hectometers
        result = await self._read(
            self._bike_profile.Movement.DISTANCE,
        )
        return int.from_bytes(result, "little") / 10

    async def get_power_level(self) -> int:
        """
        **Must be authenticated to call**

        TODO: Need to figure out what this actually returns

        :raises ``bleak.exc.BleakError``: if the client is not authenticated.

        :return: N/A
        """
        result = await self._read(
            self._bike_profile.Movement.POWER_LEVEL,
        )
        return result

    async def get_frame_number(self) -> str:
        """
        **No authentication needed to call**

        Returns the frame number of the bike.

        :raises ``bleak.exc.BleakError``: if the client is not authenticated.

        :return: A string that represents the frame number.
        """
        result = await self._read(
            self._bike_profile.BikeInfo.FRAME_NUMBER,
            needs_decryption=False,
        )

        return result.decode("ascii")

    async def get_sound_volume(self) -> int:
        """
        **Must be authenticated to call**

        Gets the sound volume. TODO: parse output

        :raises ``bleak.exc.BleakError``: if the client is not authenticated.

        :return: N/A
        """
        result = await self._read(
            self._bike_profile.Sound.SOUND_VOLUME,
        )
        return result

    async def get_speed(self) -> int:
        """
        **Must be authenticated to call**

        Gets the current speed of the bike in the units set by the bike.

        :raises ``bleak.exc.BleakError``: if the client is not authenticated.

        :return: An integer that represents the speed of the bike.
        """
        result = await self._read(
            self._bike_profile.Movement.SPEED,
        )
        return int.from_bytes(result, "little")

    async def get_light_mode(self) -> int:
        """
        **Must be authenticated to call**

        Gets the light mode. TODO: parse output

        :raises ``bleak.exc.BleakError``: if the client is not authenticated.

        :return: N/A
        """
        result = await self._read(
            self._bike_profile.Movement.SPEED,
        )
        return result
