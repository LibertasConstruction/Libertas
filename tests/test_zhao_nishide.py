# Python imports
import unittest

# Project imports
from src.zhao_nishide.zn_client import ZNClient
from src.zhao_nishide.zn_server import ZNServer


class TestSetup(unittest.TestCase):
    def test_setup(self):
        security_parameter = 2048

        client = ZNClient(.01, 6)
        client.setup(security_parameter)
        (k_h, k_g) = client.k

        self.assertEqual(client.bf_hash_functions, len(k_h))
        for k in k_h:
            self.assertEqual(security_parameter // 8, len(k))
        self.assertEqual(security_parameter // 8, len(k_g))

    def test_build_index(self):
        server = ZNServer()
        server.build_index()
        self.assertEqual([], server.index)


class TestAdd(unittest.TestCase):
    def setUp(self):
        self.client = ZNClient(.01, 6)
        self.client.setup(2048)
        self.server = ZNServer()
        self.server.build_index()

    def test_simple_add(self):
        add_token = self.client.add_token(1, 'abc')
        self.server.add(add_token)
        srch_token = self.client.srch_token('abc')
        result = self.server.search(srch_token)
        self.assertEqual([1], result)

    def test_add_multiple_keywords(self):
        keywords = ['abc', 'abcd', 'abcde', 'abcdef', 'abcdefg', 'abcdefgh', 'abcdefghi']

        for keyword in keywords:
            add_token = self.client.add_token(1, keyword)
            self.server.add(add_token)

        for keyword in keywords:
            srch_token = self.client.srch_token(keyword)
            result = self.server.search(srch_token)
            self.assertEqual([1], result)


class TestDelete(unittest.TestCase):
    def setUp(self):
        self.client = ZNClient(.01, 6)
        self.client.setup(2048)
        self.server = ZNServer()
        self.server.build_index()

        self.keywords = ['abc', 'abcd', 'abcde', 'abcdef', 'abcdefg', 'abcdefgh', 'abcdefghi']

        for keyword in self.keywords:
            add_token = self.client.add_token(1, keyword)
            self.server.add(add_token)
            add_token = self.client.add_token(2, keyword)
            self.server.add(add_token)

    def test_simple_delete(self):
        for w in self.keywords:
            del_token = self.client.del_token(1, w)
            self.server.delete(del_token)
            srch_token = self.client.srch_token(w)
            result = self.server.search(srch_token)
            self.assertTrue({2}.issubset(set(result)))
        for w in self.keywords:
            del_token = self.client.del_token(2, w)
            self.server.delete(del_token)
        srch_token = self.client.srch_token('*')
        result = self.server.search(srch_token)
        self.assertEqual([], result)

    def test_re_adding_after_delete(self):
        add_token = self.client.add_token(1, 'test')
        self.server.add(add_token)
        del_token = self.client.del_token(1, 'test')
        self.server.delete(del_token)
        re_add_token = self.client.add_token(1, 'test')
        self.server.add(re_add_token)
        srch_token = self.client.srch_token('test')
        result = self.server.search(srch_token)
        self.assertEqual([1], result)


class TestSearch(unittest.TestCase):
    def setUp(self):
        self.client = ZNClient(.01, 10)
        self.client.setup(2048)
        self.server = ZNServer()
        self.server.build_index()

    def test_search_empty_index(self):
        queries = ['abc', '_', '*', '']

        for query in queries:
            srch_token = self.client.srch_token(query)
            result = self.server.search(srch_token)
            self.assertEqual([], result)

    def test_empty_query(self):
        keywords = ['abc', 'abcd', 'abcde', 'abcdef', 'abcdefg', 'abcdefgh', 'abcdefghi', '']

        for ind, w in zip(range(len(keywords)), keywords):
            add_token = self.client.add_token(ind, w)
            self.server.add(add_token)

        srch_token = self.client.srch_token('')
        result = self.server.search(srch_token)
        self.assertTrue({7}.issubset(set(result)))

    def test_simple_search(self):
        keywords = ['abc', 'abcd', 'abcde', 'abcdef', 'abcdefg', 'abcdefgh', 'abcdefghi']

        for ind, w in zip(range(len(keywords)), keywords):
            add_token = self.client.add_token(ind, w)
            self.server.add(add_token)

        for ind, w in zip(range(len(keywords)), keywords):
            srch_token = self.client.srch_token(w)
            result = self.server.search(srch_token)
            self.assertTrue({ind}.issubset(set(result)))

    def test_search_multiple_matches(self):
        number_of_documents = 100

        for ind in range(number_of_documents):
            add_token = self.client.add_token(ind, 'abc')
            self.server.add(add_token)
        srch_token = self.client.srch_token('abc')
        result = self.server.search(srch_token)
        self.assertTrue(set(range(number_of_documents)).issubset(set(result)))

    def test_singular_wildcard(self):
        keywords = ['cat', 'cut', 'sit', 'cet', 'dot', 'cyt', 'sat']

        for ind, w in zip(range(len(keywords)), keywords):
            add_token = self.client.add_token(ind, w)
            self.server.add(add_token)

        queries = ['c_t', '__t', 'cat_', '_a_', '___']
        results = [
            [0, 1, 3, 5],
            [0, 1, 2, 3, 4, 5, 6],
            [],
            [0, 6],
            [0, 1, 2, 3, 4, 5, 6]
        ]

        for q, r in zip(queries, results):
            srch_token = self.client.srch_token(q)
            result = self.server.search(srch_token)
            self.assertTrue(set(r).issubset(result))

    def test_plural_wildcard(self):
        keywords = ['', 'test', 'testcase', 'testcasesimulator', 'testcasesimulatorproof']

        for ind, w in zip(range(len(keywords)), keywords):
            add_token = self.client.add_token(ind, w)
            self.server.add(add_token)

        queries = ['*', 'test', 'test*', '*test', '*test*', '*es*es*', '*simulator*']
        results = [
            [0, 1, 2, 3, 4],
            [1],
            [1, 2, 3, 4],
            [1],
            [1, 2, 3, 4],
            [3, 4],
            [3, 4],
        ]

        for q, r in zip(queries, results):
            srch_token = self.client.srch_token(q)
            result = self.server.search(srch_token)
            self.assertTrue(set(r).issubset(result))

    def test_date_searches(self):
        keywords = [
            '25-01-1996',
            '15-07-1996',
            '06-10-1996',
            '25-01-2000',
            '14-03-2001',
            '11-09-2001',
            '01-01-2021',
            '16-01-2021',
            '20-07-2021',
        ]

        for ind, w in zip(range(len(keywords)), keywords):
            add_token = self.client.add_token(ind, w)
            self.server.add(add_token)

        queries = ['25-01-1996', '__-__-2001', '25-01-____', '__-01-2021', '__-__-20__', '*-1996']
        results = [
            [0],
            [4, 5],
            [0, 3],
            [6, 7],
            [3, 4, 5, 6, 7, 8],
            [0, 1, 2],
        ]

        for q, r in zip(queries, results):
            srch_token = self.client.srch_token(q)
            result = self.server.search(srch_token)
            self.assertTrue(set(r).issubset(set(result)))

    def test_complex_searches(self):
        keywords = ['abc', 'aba', 'bac', 'cab', 'abcabcabc']

        for ind, w in zip(range(len(keywords)), keywords):
            add_token = self.client.add_token(ind, w)
            self.server.add(add_token)

        queries = ['*a*', 'a*', '*c', '*ab*', 'ab_', '*', '*c_bc_*', '*d*']
        results = [
            [0, 1, 2, 3, 4],
            [0, 1, 4],
            [0, 2, 4],
            [0, 1, 3, 4],
            [0, 1],
            [0, 1, 2, 3, 4],
            [4],
            [],
        ]

        for q, r in zip(queries, results):
            srch_token = self.client.srch_token(q)
            result = self.server.search(srch_token)
            self.assertTrue(set(r).issubset(result))


if __name__ == '__main__':
    unittest.main()
