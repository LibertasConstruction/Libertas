# Python imports
import hashlib
import hmac
import os

# Third-party imports
from Crypto.Cipher import AES


def hash_string(
        k: bytes,
        e: str,
) -> bytes:
    """Hash a string using SHA-256.

    :param k: Hash key
    :type k: bytes
    :param e: Hash input
    :type e: str
    :returns: The SHA-256 hash of the input string
    :rtype: bytes
    """
    return hmac.new(k, e.encode('utf-8'), hashlib.sha256).digest()


def hash_int(
        k: bytes,
        e: int,
) -> bytes:
    """Hash an integer using SHA-256.

    :param k: Hash key
    :type k: bytes
    :param e: Hash input
    :type e: int
    :returns: The SHA-256 hash of the input integer
    :rtype: bytes
    """
    return hash_string(k, str(e))


def hash_bytes(
        k: bytes,
        e: bytes,
) -> bytes:
    """Hash bytes using SHA-256.

    :param k: Hash key
    :type k: bytes
    :param e: Hash input
    :type e: bytes
    :returns: The SHA-256 hash of the input bytes
    :rtype: bytes
    """
    return hmac.new(k, e, hashlib.sha256).digest()


def hash_string_to_int(
        k: bytes,
        e: str,
) -> int:
    """Hash a string using SHA-256 and convert the result to an integer.

    :param k: Hash key
    :type k: bytes
    :param e: Hash input
    :type e: str
    :returns: An integer representation of the SHA-256 hash of the input string
    :rtype: int
    """
    return int.from_bytes(hash_string(k, e), 'big')


def encrypt(
        key: bytes,
        plain_text: str,
) -> bytes:
    """Encrypts data using AES in CBC mode.

    :param key: The encryption key
    :type key: bytes
    :param plain_text: The data to encrypt
    :type plain_text: str
    :returns: The encryption of the raw data
    :rtype: bytes
    """
    block_size = 16
    plain_text = _pad(plain_text, block_size)
    iv = os.urandom(block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(plain_text.encode())
    return iv + cipher_text


def decrypt(
        key: bytes,
        cipher_text: bytes,
) -> str:
    """Decrypts cipher text using AES in CBC mode.

    :param key: The decryption key
    :type key: bytes
    :param cipher_text: The cipher text to decrypt
    :type cipher_text: bytes
    :returns: The decryption of the cipher text
    :rtype: str
    """
    block_size = 16
    iv = cipher_text[:block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plain_text = cipher.decrypt(cipher_text[block_size:]).decode('utf-8')
    return _unpad(plain_text)


def _pad(
        s: str,
        bs: int,
) -> str:
    """Pads a string so its length is a multiple of a specified block size.

    :param s: The string that is to be padded
    :type s: str
    :param bs: The block size
    :type bs: int
    :returns: The initial string, padded to have a length that is a multiple of the specified block size
    :rtype: str
    """
    number_of_bytes_to_pad = bs - len(s) % bs
    ascii_string = chr(number_of_bytes_to_pad)
    padding_str = number_of_bytes_to_pad * ascii_string
    return s + padding_str


def _unpad(
        s: str,
) -> str:
    """Unpads a string that was previously padded by _pad().

    :param s: The string to unpad
    :type s: bytes
    :returns: The unpadded string
    :rtype: str
    """
    last_character = s[len(s) - 1:]
    bytes_to_remove = ord(last_character)
    return s[:-bytes_to_remove]
