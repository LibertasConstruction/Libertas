# Python imports
import os
import unittest

# Project imports
from src.crypto import encrypt, decrypt


class TestEncrypt(unittest.TestCase):
    def test_encryptions(self):
        keys = [os.urandom(128 // 8), os.urandom(192 // 8), os.urandom(256 // 8)]
        plain_texts = ['test', '1234', 'this is a rather short sentence.', '''Lorem ipsum dolor sit amet, consectetur
        adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
        quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in
        reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
        non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.''']

        for key in keys:
            for plain_text in plain_texts:
                cipher_text = encrypt(key, plain_text)
                result = decrypt(key, cipher_text)
                self.assertEqual(plain_text, result)


if __name__ == '__main__':
    unittest.main()
