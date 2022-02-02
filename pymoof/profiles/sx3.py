import enum
import math

from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import modes


class SX3Profile:
    """
    Represents the profile for the GATT UUIDs for the S3/X3. Also contains functionality
    to encrypt and decrypt BLE payloads, as well as building the authentication payload.

    :param key: The hexidecimal string of the encrypted key from Vanmoof servers.
    """

    def __init__(self, key: str) -> None:
        self._cipher = Cipher(algorithms.AES(bytes.fromhex(key)), modes.ECB())

    def build_authentication_payload(self, nonce: bytes) -> bytes:
        """
        Builds the authentication payload given a nonce.

        :param nonce: A bytes array that represents the nonce from a challenge response.
        """
        encryptor = self._cipher.encryptor()

        data = bytearray(16)
        data[0:2] = nonce
        data = bytearray(encryptor.update(data) + encryptor.finalize())

        # unknown why we need to append these 4 bytes _after_ encryption
        data.extend([0, 0, 0, 2])

        return bytes(data)

    def decrypt_payload(self, data: bytes) -> bytes:
        """
        Decrypts a bluetooth payload.

        :param data: A bytes array of data. Must be a multiple of 16 bytes long.
        """
        decryptor = self._cipher.decryptor()
        return decryptor.update(data) + decryptor.finalize()

    def build_encrypted_payload(self, nonce: bytes, data: bytes) -> bytes:
        """
        Encrypts data signed with a nonce. This will build a payload and pad with
        zeroes to the nearest multiple of 16 bytes.

        :param nonce: A bytes array that represents the nonce from a challenge response.
        :param data: A bytes array of data.
        """
        encryptor = self._cipher.encryptor()

        payload = bytearray(16)
        payload[0:2] = nonce
        payload[2:] = data

        # Pad to the nearest cipher 16 byte block size
        for _ in range(math.ceil(len(payload) / 16) * 16 - len(payload)):
            payload.append(0)

        return bytes(encryptor.update(payload) + encryptor.finalize())

    class Security(enum.Enum):

        SERVICE_UUID = "6acc5500-e631-4069-944d-b8ca7598ad50"

        CHALLENGE = "6acc5501-e631-4069-944d-b8ca7598ad50"
        KEY_INDEX = "6acc5502-e631-4069-944d-b8ca7598ad50"
        BACKUP_CODE = "6acc5503-e631-4069-944d-b8ca7598ad50"
        BIKE_MESSAGE = "6acc5505-e631-4069-944d-b8ca7598ad50"

    class Defense(enum.Enum):

        SERVICE_UUID = "6acc5520-e631-4069-944d-b8ca7598ad50"

        LOCK_STATE = "6acc5521-e631-4069-944d-b8ca7598ad50"
        UNLOCK_REQUEST = "6acc5522-e631-4069-944d-b8ca7598ad50"
        ALARM_STATE = "6acc5523-e631-4069-944d-b8ca7598ad50"
        ALARM_MODE = "6acc5524-e631-4069-944d-b8ca7598ad50"

    class Movement(enum.Enum):

        SERVICE_UUID = "6acc5530-e631-4069-944d-b8ca7598ad50"

        DISTANCE = "6acc5531-e631-4069-944d-b8ca7598ad50"
        SPEED = "6acc5532-e631-4069-944d-b8ca7598ad50"
        UNIT_SYSTEM = "6acc5533-e631-4069-944d-b8ca7598ad50"
        POWER_LEVEL = "6acc5534-e631-4069-944d-b8ca7598ad50"
        SPEED_LIMIT = "6acc5535-e631-4069-944d-b8ca7598ad50"
        E_SHIFTER_GEAR = "6acc5536-e631-4069-944d-b8ca7598ad50"
        E_SHIFTIG_POINTS = "6acc5537-e631-4069-944d-b8ca7598ad50"
        E_SHIFTER_MODE = "6acc5538-e631-4069-944d-b8ca7598ad50"

    class BikeInfo(enum.Enum):

        SERVICE_UUID = "6acc5540-e631-4069-944d-b8ca7598ad50"

        MOTOR_BATTERY_LEVEL = "6acc5541-e631-4069-944d-b8ca7598ad50"
        MOTOR_BATTERY_STATE = "6acc5542-e631-4069-944d-b8ca7598ad50"
        MODULE_BATTERY_LEVEL = "6acc5543-e631-4069-944d-b8ca7598ad50"
        MODULE_BATTERY_STATE = "6acc5544-e631-4069-944d-b8ca7598ad50"
        BIKE_FIRMWARE_VERSION = "6acc554a-e631-4069-944d-b8ca7598ad50"
        BLE_CHIP_FIRMWARE_VERSION = "6acc554b-e631-4069-944d-b8ca7598ad50"
        CONTROLLER_FIRMWARE_VERSION = "6acc554c-e631-4069-944d-b8ca7598ad50"
        PCBA_HARDWARE_VERSION = "6acc554d-e631-4069-944d-b8ca7598ad50"
        GSM_FIRMWARE_VERSION = "6acc554e-e631-4069-944d-b8ca7598ad50"
        E_SHIFTER_FIRMWARE_VERSION = "6acc554f-e631-4069-944d-b8ca7598ad50"
        BATTERY_FIRMWARE_VERSION = "6acc5550-e631-4069-944d-b8ca7598ad50"

        # data returned seems to be firmware version info?
        _UNKNOWN = "6acc5551-e631-4069-944d-b8ca7598ad50"

        FRAME_NUMBER = "6acc5552-e631-4069-944d-b8ca7598ad50"

    class BikeState(enum.Enum):

        SERVICE_UUID = "6acc5560-e631-4069-944d-b8ca7598ad50"

        MODULE_MODE = "6acc5561-e631-4069-944d-b8ca7598ad50"
        MODULE_STATE = "6acc5562-e631-4069-944d-b8ca7598ad50"
        ERRORS = "6acc5563-e631-4069-944d-b8ca7598ad50"
        WHEEL_SIZE = "6acc5564-e631-4069-944d-b8ca7598ad50"
        CLOCK = "6acc5567-e631-4069-944d-b8ca7598ad50"

    class Sound(enum.Enum):

        SERVICE_UUID = "6acc5570-e631-4069-944d-b8ca7598ad50"

        PLAY_SOUND = "6acc5571-e631-4069-944d-b8ca7598ad50"
        SOUND_VOLUME = "6acc5572-e631-4069-944d-b8ca7598ad50"
        BELL_SOUND = "6acc5574-e631-4069-944d-b8ca7598ad50"

    class Light(enum.Enum):

        SERVICE_UUID = "6acc5580-e631-4069-944d-b8ca7598ad50"

        LIGHT_MODE = "6acc5581-e631-4069-944d-b8ca7598ad50"
        SENSOR = "6acc5584-e631-4069-944d-b8ca7598ad50"
