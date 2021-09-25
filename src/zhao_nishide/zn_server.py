# Python imports
from typing import List, Tuple

# Third-party imports
from bitarray import bitarray

# Project imports
from src.crypto import hash_bytes
from src.sigma_interface.sigma_server import SigmaServer


class ZNServer(SigmaServer[Tuple[bytes, bitarray, bytes], Tuple[List[int], List[bytes]]]):
    """Zhao and Nishide server implementation.

    Based on: Fangming Zhao and Takashi Nishide. Searchable symmetric encryption supporting queries with
    multiple-character wildcards. In International Conference on Network and System Security, pages 266–282. Springer,
    2016.

    This implementation uses Bloom filters for the index. Search queries are allowed to contain both _ and * wildcard
    characters. A _ character is used to indicate the presence of any single character, while the * character marks the
    presence of 0 or more characters.
    """

    def __init__(
            self,
    ) -> None:
        """Initializes a Zhao and Nishide server.

        :returns: None
        :rtype: None
        """
        super().__init__()
        self.index = None

    def build_index(
            self,
    ) -> None:
        """Sets up the Z&N server, creating an empty index.

        :returns: None
        :rtype: None
        """
        self.index: List[(bytes, bitarray)] = []

    def search(
            self,
            srch_token: Tuple[List[int], List[bytes]],
    ) -> List[int]:
        """Searches the index for a query represented by a search token and returns matching document IDs.
        The first part of a search token consists of Bloom filter positions, one per element in s_t(q). The second part
        of a search token consists of hashes of these positions.

        :param srch_token: The search token
        :type srch_token: Tuple[List[int], List[bytes]]
        :returns: A list containing the identifiers of matching documents and possibly some other documents, as the
        use of Bloom filters introduce false positives.
        :rtype: List[int]
        """
        (td1s, td2s) = srch_token
        results = []
        for ind, bit_array, b_id in self.index:
            for pos, h_pos in zip(td1s, td2s):
                mask_bit = hash_bytes(b_id, h_pos)[0] & 1
                if bit_array[pos] ^ mask_bit == 0:
                    break
            else:
                if ind not in results:
                    results.append(ind)
        return results

    def add(
            self,
            add_token: Tuple[int, bitarray, bytes],
    ) -> None:
        """Adds a document-keyword pair, represented by an add token, to the index.
        An add token consists of a document identifier, a Bloom filter and its ID.

        :param add_token: An add token representing a document-keyword pair
        :type add_token: Tuple[int, bitarray, bytes]
        :returns: None
        :rtype: None
        """
        self.index.append(add_token)

    def delete(
            self,
            del_token: bytes,
    ) -> None:
        """Deletes a document-keyword pair, represented by a delete token, from the index.
        A delete token is a Bloom filter ID.

        :param del_token: A delete token representing a document-keyword pair
        :type del_token: bytes
        :returns: None
        :rtype: None
        """
        self.index = [(ind, bf, b_id) for (ind, bf, b_id) in self.index if b_id != del_token]
