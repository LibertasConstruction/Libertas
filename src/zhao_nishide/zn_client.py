# Python imports
import math
import os
from typing import List, Tuple

# Third-party imports
from bitarray import bitarray

# Project imports
from src.crypto import hash_string_to_int, hash_int, hash_string, hash_bytes
from src.sigma_interface.sigma_client import SigmaClient


class ZNClient(SigmaClient[Tuple[bytes, bitarray, bytes], Tuple[List[int], List[bytes]]]):
    """Zhao and Nishide client implementation.

    Based on: Fangming Zhao and Takashi Nishide. Searchable symmetric encryption supporting queries with
    multiple-character wildcards. In International Conference on Network and System Security, pages 266–282. Springer,
    2016.

    This implementation uses Bloom filters for the index. Search queries are allowed to contain both _ and * wildcard
    characters. A _ character is used to indicate the presence of any single character, while the * character marks the
    presence of 0 or more characters.
    """

    def __init__(
            self,
            fp_rate: float,
            average_keyword_length: int,
    ) -> None:
        """Initializes a Zhao and Nishide client.

        :param fp_rate: The false-positive rate of individual search results
        :type fp_rate: float
        :param average_keyword_length: The average length of keywords, used to determine optimal Bloom filter parameters
        :returns: None
        :rtype: None
        """
        super().__init__()

        # Estimate optimal Bloom filter parameters
        set_size = len(self._s_k('0' * average_keyword_length))
        self.bf_size = math.ceil(-(set_size * math.log(fp_rate)) / (math.log(2) ** 2))
        self.bf_hash_functions = math.ceil((self.bf_size / set_size) * math.log(2))

        self.k = None

    def setup(
            self,
            security_parameter: int,
    ) -> None:
        """Sets up the Z&N client, generating keys k_h and k_g.

        :param security_parameter: The required security strength (bits)
        :type security_parameter: int
        :returns: None
        :rtype: None
        """
        k_h: List[bytes] = [os.urandom(security_parameter // 8) for _ in range(self.bf_hash_functions)]
        k_g: bytes = os.urandom(security_parameter // 8)
        self.k: (bytes, bytes) = (k_h, k_g)

    def srch_token(
            self,
            q: str,
    ) -> Tuple[List[int], List[bytes]]:
        """Creates a search token for a query, to be send to a Z&N server.
        The first part of the search token consists of Bloom filter positions, one per element in s_t(q).
        The second part of the search token consists of hashes of these positions.

        :param q: The query, a string of characters, possibly containing singular _ and * wildcards
        :type q: str
        :returns: The search token
        :rtype: (List[int], List[bytes])
        """
        (k_h, k_g) = self.k
        # Append the query with '\0' to indicate the end of the query. This way 'test' is interpreted differently from
        # 'test*'.
        s_t = self._s_t(q + '\0')
        td1s: List[int] = [hash_string_to_int(k, e) % self.bf_size for e in s_t for k in k_h]
        td2s: List[bytes] = [hash_int(k_g, pos) for pos in td1s]
        return td1s, td2s

    def add_token(
            self,
            ind: int,
            w: str,
    ) -> Tuple[int, bitarray, bytes]:
        """Creates an add token for a document-keyword pair, to be send to a Z&N server.
        Add tokens consist of the document identifier, Bloom filter and its ID.

        :param ind: The document identifier of the document-keyword pair to add
        :type ind: int
        :param w: The keyword of the document-keyword pair to add
        :type w: str
        :returns: An add token, a tuple consisting of a document identifier, Bloom filter and its ID
        :rtype: Tuple[int, bitarray, bytes]
        """
        # Append the keyword with '\0' to indicate the end of the keyword
        s_k = self._s_k(w + '\0')
        (k_h, k_g) = self.k
        b_id = hash_string(k_g, str(ind) + w)
        bloom_filter = bitarray(self.bf_size)

        # Fill Bloom filter
        for e in s_k:
            for k in k_h:
                pos = hash_string_to_int(k, e) % self.bf_size
                bloom_filter[pos] = True

        # Mask Bloom filter
        for pos in range(self.bf_size):
            h = hash_bytes(b_id, hash_int(k_g, pos))
            first_hash_bit = h[0] & 1
            bloom_filter[pos] ^= first_hash_bit
        return ind, bloom_filter, b_id

    def del_token(
            self,
            ind: int,
            w: str,
    ) -> bytes:
        """Creates a delete token for a document-keyword pair, to be send to a Z&N server.
        A delete token is a Bloom filter ID.

        :param ind: The document identifier of the document-keyword pair to delete
        :type ind: int
        :param w: The keyword of the document-keyword pair to delete
        :type w: str
        :returns: A delete token, which is a Bloom filter ID
        :rtype: bytes
        """
        (_, k_g) = self.k
        b_id = hash_string(k_g, str(ind) + w)
        return b_id

    @classmethod
    def _s_k(
            cls,
            w: str,
    ) -> List[str]:
        """Generates the S_K set for a keyword.

        :param w: The keyword for which the set is to be generated
        :type w: str
        :returns: The S_K set of the keyword
        :rtype: List[str]
        """
        return cls._s_k_o(w) + cls._s_k_p(w)

    @classmethod
    def _s_k_o(
            cls,
            w: str,
    ) -> List[str]:
        """Generates the S_K^(o) set for a keyword.
        Set items are of the form '{position}:{character}'.

        :param w: The keyword for which the set is to be generated
        :type w: str
        :returns: The S_K^(o) set of the keyword
        :rtype: List[str]
        """
        return [str(n + 1) + ':' + c for n, c in zip(range(len(w)), w)]

    @classmethod
    def _s_k_p(
            cls,
            w: str,
    ) -> List[str]:
        """Generates the S_K^(p) set for a keyword.

        :param w: The keyword for which the set is to be generated
        :type w: str
        :returns: The S_K set of the keyword
        :rtype: List[str]
        """
        return cls._s_k_p1(w) + cls._s_k_p2(w)

    @classmethod
    def _s_k_p1(
            cls,
            w: str,
    ) -> List[str]:
        """Generates the S_K^(p1) set for a keyword.
        Set items are of the form '{occurrence}:{character distance}:{character 1},{character 2}'.

        :param w: The keyword for which the set is to be generated
        :type w: str
        :returns: The S_K^(p1) set of the keyword
        :rtype: List[str]
        """
        # Generate '{character distance}:{character 1},{character 2}' for every character pair in the keyword
        pairs = [str(c2 - c1) + ':' + w[c1] + ',' + w[c2]
                 for c1 in range(len(w))
                 for c2 in range(c1 + 1, len(w))]

        # Append '{occurrence}:'
        unique_pairs = list(set(pairs))
        pair_count_dict = {pair: pairs.count(pair) for pair in unique_pairs}
        return [str(count + 1) + ':' + pair
                for pair in pair_count_dict.keys()
                for count in range(pair_count_dict[pair])]

    @classmethod
    def _s_k_p2(
            cls,
            w: str,
    ) -> List[str]:
        """Generates the S_K^(p2) set for a keyword.
        Set items are of the form '{occurrence}:{character 1},{character 2}'.

        :param w: The keyword for which the set is to be generated
        :type w: str
        :returns: The S_K^(p2) set of the keyword
        :rtype: List[str]
        """
        # Generate '{character 1},{character 2}' for every character pair in the keyword
        pairs = [w[c1] + ',' + w[c2]
                 for c1 in range(len(w))
                 for c2 in range(c1 + 1, len(w))]

        # Append '{occurrence}:'
        unique_pairs = list(set(pairs))
        pair_count_dict = {pair: pairs.count(pair) for pair in unique_pairs}
        return [str(count + 1) + ':' + pair
                for pair in pair_count_dict.keys()
                for count in range(pair_count_dict[pair])]

    @classmethod
    def _s_t(
            cls,
            q: str,
    ) -> List[str]:
        """Generates the S_T set for a keyword.

        :param q: The query for which the set is to be generated
        :type q: str
        :returns: The S_T set of the query
        :rtype: List[str]
        """
        return cls._s_t_o(q) + cls._s_t_p(q)

    @classmethod
    def _s_t_o(
            cls,
            q: str,
    ) -> List[str]:
        """Generates the S_T^(o) set for a query.
        Set items are of the form '{position}:{character}' and contain all characters in the query that have a specific
        appearance order, which are all characters (except the _ wildcard), up until the first * wildcard.

        :param q: The query for which the set is to be generated. A string, possibly containing _ and * wildcards
        :type q: str
        :returns: The S_T^(o) set of the query
        :rtype: List[str]
        """
        fixed_characters = q.split('*')[0]
        return [str(c + 1) + ':' + q[c] for c in range(len(fixed_characters)) if q[c] != '_']

    @classmethod
    def _s_t_p(
            cls,
            q: str,
    ) -> List[str]:
        """Generates the S_T^(p) set for a keyword.

        :param q: The query for which the set is to be generated
        :type q: str
        :returns: The S_T set of the query
        :rtype: List[str]
        """
        return cls._s_t_p1(q) + cls._s_t_p2(q)

    @classmethod
    def _s_t_p1(
            cls,
            q: str,
    ) -> List[str]:
        """Generates the S_T^(p1) set for a query.
        Set items are of the form '{occurrence}:{character distance}:{character 1},{character 2}'

        :param q: The query for which the set is to be generated
        :type q: str
        :returns: The S_T^(p1) set of the query
        :rtype: List[str]
        """
        consecutive_character_groups = q.split('*')
        # Generate all pairs of characters within a consecutive character group as
        # '{character distance}:{character 1},{character 2}'
        pairs = [str(c2 - c1) + ':' + group[c1] + ',' + group[c2]
                 for group in consecutive_character_groups
                 for c1 in range(len(group)) if group[c1] != '_'
                 for c2 in range(c1 + 1, len(group)) if group[c2] != '_']

        # Append '{occurrence}:'
        unique_pairs = list(set(pairs))
        pair_count_dict = {pair: pairs.count(pair) for pair in unique_pairs}
        return [str(count + 1) + ':' + pair
                for pair in pair_count_dict.keys()
                for count in range(pair_count_dict[pair])]

    @classmethod
    def _s_t_p2(
            cls,
            q: str,
    ) -> List[str]:
        """Generates the S_T^(p2) set for a query.
        Set items are of the form '{occurrence}:{character 1},{character 2}'

        :param q: The query for which the set is to be generated
        :type q: str
        :returns: The S_T^(p2) set of the query
        :rtype: List[str]
        """
        return cls._s_k_p2(q.replace('*', '').replace('_', ''))
