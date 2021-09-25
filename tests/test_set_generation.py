# Python imports
import unittest

# Project imports
from src.zhao_nishide.zn_client import ZNClient


class TestSKo(unittest.TestCase):
    def setUp(self):
        self.client = ZNClient(.01, 7)

    def test_simple_keyword(self):
        result = self.client._s_k_o('keyword')
        self.assertEqual(
            sorted([
                '1:k',
                '2:e',
                '3:y',
                '4:w',
                '5:o',
                '6:r',
                '7:d',
            ]),
            sorted(result))

    def test_empty_keyword(self):
        result = self.client._s_k_o('')
        self.assertEqual([], result)

    def test_repeating_keyword(self):
        result = self.client._s_k_o('keykey')
        self.assertEqual(
            sorted([
                '1:k',
                '2:e',
                '3:y',
                '4:k',
                '5:e',
                '6:y',
            ]),
            sorted(result)
        )


class TestSKp1(unittest.TestCase):
    def setUp(self):
        self.client = ZNClient(.01, 7)

    def test_simple_keyword(self):
        result = self.client._s_k_p1('keyword')
        self.assertEqual(
            sorted([
                '1:1:k,e',
                '1:2:k,y',
                '1:3:k,w',
                '1:4:k,o',
                '1:5:k,r',
                '1:6:k,d',
                '1:1:e,y',
                '1:2:e,w',
                '1:3:e,o',
                '1:4:e,r',
                '1:5:e,d',
                '1:1:y,w',
                '1:2:y,o',
                '1:3:y,r',
                '1:4:y,d',
                '1:1:w,o',
                '1:2:w,r',
                '1:3:w,d',
                '1:1:o,r',
                '1:2:o,d',
                '1:1:r,d',
            ]),
            sorted(result)
        )

    def test_empty_keyword(self):
        result = self.client._s_k_p1('')
        self.assertEqual(result, [])

    def test_repeating_keyword(self):
        result = self.client._s_k_p1('keykey')
        self.assertEqual(
            sorted([
                '1:1:k,e',
                '1:2:k,y',
                '1:3:k,k',
                '1:4:k,e',
                '1:5:k,y',
                '1:1:e,y',
                '1:2:e,k',
                '1:3:e,e',
                '1:4:e,y',
                '1:1:y,k',
                '1:2:y,e',
                '1:3:y,y',
                '2:1:k,e',
                '2:2:k,y',
                '2:1:e,y',
            ]),
            sorted(result)
        )


class TestSKp2(unittest.TestCase):
    def setUp(self):
        self.client = ZNClient(.01, 7)

    def test_simple_keyword(self):
        result = self.client._s_k_p2('keyword')
        self.assertEqual(
            sorted([
                '1:k,e',
                '1:k,y',
                '1:k,w',
                '1:k,o',
                '1:k,r',
                '1:k,d',
                '1:e,y',
                '1:e,w',
                '1:e,o',
                '1:e,r',
                '1:e,d',
                '1:y,w',
                '1:y,o',
                '1:y,r',
                '1:y,d',
                '1:w,o',
                '1:w,r',
                '1:w,d',
                '1:o,r',
                '1:o,d',
                '1:r,d',
            ]),
            sorted(result)
        )

    def test_empty_keyword(self):
        result = self.client._s_k_p2('')
        self.assertEqual(result, [])

    def test_repeating_keyword(self):
        result = self.client._s_k_p2('keykey')
        self.assertEqual(
            sorted([
                '1:k,e',
                '1:k,y',
                '1:k,k',
                '2:k,e',
                '2:k,y',
                '1:e,y',
                '1:e,k',
                '1:e,e',
                '2:e,y',
                '1:y,k',
                '1:y,e',
                '1:y,y',
                '3:k,e',
                '3:k,y',
                '3:e,y',
            ]),
            sorted(result)
        )


class TestSTo(unittest.TestCase):
    def setUp(self):
        self.client = ZNClient(.01, 7)

    def test_simple_query(self):
        result = self.client._s_t_o('keyword')
        self.assertEqual(
            sorted([
                '1:k',
                '2:e',
                '3:y',
                '4:w',
                '5:o',
                '6:r',
                '7:d',
            ]),
            sorted(result)
        )

    def test_empty_query(self):
        result = self.client._s_t_o('')
        self.assertEqual(result, [])

    def test_repeating_query(self):
        result = self.client._s_t_o('keykey')
        self.assertEqual(
            sorted([
                '1:k',
                '2:e',
                '3:y',
                '4:k',
                '5:e',
                '6:y',
            ]),
            sorted(result)
        )
    
    def test_simple_singular_wildcard_query(self):
        result = self.client._s_t_o('key_ord')
        self.assertEqual(
            sorted([
                '1:k',
                '2:e',
                '3:y',
                '5:o',
                '6:r',
                '7:d',
            ]),
            sorted(result)
        )

    def test_simple_plural_wildcard_query(self):
        result = self.client._s_t_o('key*word')
        self.assertEqual(
            sorted([
                '1:k',
                '2:e',
                '3:y',
            ]),
            sorted(result)
        )

    def test_query_starting_with_plural_wildcard(self):
        result = self.client._s_t_o('*keyword')
        self.assertEqual(result, [])

    def test_singular_wildcard_only_query(self):
        result = self.client._s_t_o('_')
        self.assertEqual(result, [])

    def test_plural_wildcard_only_query(self):
        result = self.client._s_t_o('*')
        self.assertEqual(result, [])

    def test_wildcard_rich_query(self):
        result = self.client._s_t_o('_ke_w__d**k_yw*rd')
        self.assertEqual(
            sorted([
                '2:k',
                '3:e',
                '5:w',
                '8:d',
            ]),
            sorted(result)
        )


class TestSTp1(unittest.TestCase):

    def setUp(self):
        self.client = ZNClient(.01, 7)

    def test_simple_keyword(self):
        result = self.client._s_t_p1('keyword')
        self.assertEqual(
            sorted([
                '1:1:k,e',
                '1:2:k,y',
                '1:3:k,w',
                '1:4:k,o',
                '1:5:k,r',
                '1:6:k,d',
                '1:1:e,y',
                '1:2:e,w',
                '1:3:e,o',
                '1:4:e,r',
                '1:5:e,d',
                '1:1:y,w',
                '1:2:y,o',
                '1:3:y,r',
                '1:4:y,d',
                '1:1:w,o',
                '1:2:w,r',
                '1:3:w,d',
                '1:1:o,r',
                '1:2:o,d',
                '1:1:r,d',
            ]),
            sorted(result)
        )

    def test_empty_keyword(self):
        result = self.client._s_t_p1('')
        self.assertEqual(result, [])

    def test_repeating_keyword(self):
        result = self.client._s_t_p1('keykey')
        self.assertEqual(
            sorted([
                '1:1:k,e',
                '1:2:k,y',
                '1:3:k,k',
                '1:4:k,e',
                '1:5:k,y',
                '1:1:e,y',
                '1:2:e,k',
                '1:3:e,e',
                '1:4:e,y',
                '1:1:y,k',
                '1:2:y,e',
                '1:3:y,y',
                '2:1:k,e',
                '2:2:k,y',
                '2:1:e,y',
            ]),
            sorted(result)
        )

    def test_simple_singular_wildcard_query(self):
        result = self.client._s_t_p1('key_ord')
        self.assertEqual(
            sorted([
                '1:1:k,e',
                '1:2:k,y',
                '1:4:k,o',
                '1:5:k,r',
                '1:6:k,d',
                '1:1:e,y',
                '1:3:e,o',
                '1:4:e,r',
                '1:5:e,d',
                '1:2:y,o',
                '1:3:y,r',
                '1:4:y,d',
                '1:1:o,r',
                '1:2:o,d',
                '1:1:r,d',
            ]),
            sorted(result)
        )

    def test_simple_plural_wildcard_query(self):
        result = self.client._s_t_p1('key*ord')
        self.assertEqual(
            sorted([
                '1:1:k,e',
                '1:2:k,y',
                '1:1:e,y',
                '1:1:o,r',
                '1:2:o,d',
                '1:1:r,d',
            ]),
            sorted(result)
        )

    def test_complex_wildcard_query(self):
        result = self.client._s_t_p1('_ey*_r_*keyword_k*word')
        self.assertEqual(
            sorted([
                '1:1:e,y',

                '1:1:k,e',
                '1:2:k,y',
                '1:3:k,w',
                '1:4:k,o',
                '1:5:k,r',
                '1:6:k,d',
                '1:8:k,k',
                '2:1:e,y',
                '1:2:e,w',
                '1:3:e,o',
                '1:4:e,r',
                '1:5:e,d',
                '1:7:e,k',
                '1:1:y,w',
                '1:2:y,o',
                '1:3:y,r',
                '1:4:y,d',
                '1:6:y,k',
                '1:1:w,o',
                '1:2:w,r',
                '1:3:w,d',
                '1:5:w,k',
                '1:1:o,r',
                '1:2:o,d',
                '1:4:o,k',
                '1:1:r,d',
                '1:3:r,k',
                '1:2:d,k',

                '2:1:w,o',
                '2:2:w,r',
                '2:3:w,d',
                '2:1:o,r',
                '2:2:o,d',
                '2:1:r,d',
            ]),
            sorted(result)
        )


class TestSTp2(unittest.TestCase):
    def setUp(self):
        self.client = ZNClient(.01, 7)

    def test_simple_keyword(self):
        result = self.client._s_t_p2('keyword')
        self.assertEqual(
            sorted([
                '1:k,e',
                '1:k,y',
                '1:k,w',
                '1:k,o',
                '1:k,r',
                '1:k,d',
                '1:e,y',
                '1:e,w',
                '1:e,o',
                '1:e,r',
                '1:e,d',
                '1:y,w',
                '1:y,o',
                '1:y,r',
                '1:y,d',
                '1:w,o',
                '1:w,r',
                '1:w,d',
                '1:o,r',
                '1:o,d',
                '1:r,d',
            ]),
            sorted(result)
        )

    def test_empty_keyword(self):
        result = self.client._s_t_p2('')
        self.assertEqual(result, [])

    def test_repeating_keyword(self):
        result = self.client._s_t_p2('keykey')
        self.assertEqual(
            sorted([
                '1:k,e',
                '1:k,y',
                '1:k,k',
                '2:k,e',
                '2:k,y',
                '1:e,y',
                '1:e,k',
                '1:e,e',
                '2:e,y',
                '1:y,k',
                '1:y,e',
                '1:y,y',
                '3:k,e',
                '3:k,y',
                '3:e,y',
            ]),
            sorted(result)
        )

    def test_simple_singular_wildcard_query(self):
        result = self.client._s_t_p2('key_ord')
        self.assertEqual(
            sorted([
                '1:k,e',
                '1:k,y',
                '1:k,o',
                '1:k,r',
                '1:k,d',
                '1:e,y',
                '1:e,o',
                '1:e,r',
                '1:e,d',
                '1:y,o',
                '1:y,r',
                '1:y,d',
                '1:o,r',
                '1:o,d',
                '1:r,d',
            ]),
            sorted(result)
        )

    def test_simple_plural_wildcard_query(self):
        result = self.client._s_t_p2('key*ord')
        self.assertEqual(
            sorted([
                '1:k,e',
                '1:k,y',
                '1:k,o',
                '1:k,r',
                '1:k,d',
                '1:e,y',
                '1:e,o',
                '1:e,r',
                '1:e,d',
                '1:y,o',
                '1:y,r',
                '1:y,d',
                '1:o,r',
                '1:o,d',
                '1:r,d',
            ]),
            sorted(result)
        )

    def test_complex_wildcard_query(self):
        result = self.client._s_t_p2('_k**y*_ordk_ywor_*dkeywo__rd')
        self.assertEqual(
            sorted([
                '1:k,y',
                '1:k,o',
                '1:k,r',
                '1:k,d',
                '1:k,k',
                '2:k,y',
                '1:k,w',
                '2:k,o',
                '2:k,r',
                '2:k,d',
                '2:k,k',
                '1:k,e',
                '3:k,y',
                '2:k,w',
                '3:k,o',
                '3:k,r',
                '3:k,d',

                '1:y,o',
                '1:y,r',
                '1:y,d',
                '1:y,k',
                '1:y,y',
                '1:y,w',
                '2:y,o',
                '2:y,r',
                '2:y,d',
                '2:y,k',
                '1:y,e',
                '2:y,y',
                '2:y,w',
                '3:y,o',
                '3:y,r',
                '3:y,d',

                '1:o,r',
                '1:o,d',
                '1:o,k',
                '1:o,y',
                '1:o,w',
                '1:o,o',
                '2:o,r',
                '2:o,d',
                '2:o,k',
                '1:o,e',
                '2:o,y',
                '2:o,w',
                '2:o,o',
                '3:o,r',
                '3:o,d',

                '1:r,d',
                '1:r,k',
                '1:r,y',
                '1:r,w',
                '1:r,o',
                '1:r,r',
                '2:r,d',
                '2:r,k',
                '1:r,e',
                '2:r,y',
                '2:r,w',
                '2:r,o',
                '2:r,r',
                '3:r,d',

                '1:d,k',
                '1:d,y',
                '1:d,w',
                '1:d,o',
                '1:d,r',
                '1:d,d',
                '2:d,k',
                '1:d,e',
                '2:d,y',
                '2:d,w',
                '2:d,o',
                '2:d,r',
                '2:d,d',

                '4:k,y',
                '3:k,w',
                '4:k,o',
                '4:k,r',
                '4:k,d',
                '3:k,k',
                '2:k,e',
                '5:k,y',
                '4:k,w',
                '5:k,o',
                '5:k,r',
                '5:k,d',

                '3:y,w',
                '4:y,o',
                '4:y,r',
                '4:y,d',
                '3:y,k',
                '2:y,e',
                '3:y,y',
                '4:y,w',
                '5:y,o',
                '5:y,r',
                '5:y,d',

                '1:w,o',
                '1:w,r',
                '1:w,d',
                '1:w,k',
                '1:w,e',
                '1:w,y',
                '1:w,w',
                '2:w,o',
                '2:w,r',
                '2:w,d',

                '4:o,r',
                '4:o,d',
                '3:o,k',
                '2:o,e',
                '3:o,y',
                '3:o,w',
                '3:o,o',
                '5:o,r',
                '5:o,d',

                '4:r,d',
                '3:r,k',
                '2:r,e',
                '3:r,y',
                '3:r,w',
                '3:r,o',
                '3:r,r',
                '5:r,d',

                '3:d,k',
                '2:d,e',
                '3:d,y',
                '3:d,w',
                '3:d,o',
                '3:d,r',
                '3:d,d',

                '3:k,e',
                '6:k,y',
                '5:k,w',
                '6:k,o',
                '6:k,r',
                '6:k,d',

                '1:e,y',
                '1:e,w',
                '1:e,o',
                '1:e,r',
                '1:e,d',

                '5:y,w',
                '6:y,o',
                '6:y,r',
                '6:y,d',

                '3:w,o',
                '3:w,r',
                '3:w,d',

                '6:o,r',
                '6:o,d',

                '6:r,d',
            ]),
            sorted(result)
        )


if __name__ == '__main__':
    unittest.main()
