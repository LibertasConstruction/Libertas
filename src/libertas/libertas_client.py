# Python imports
import math
import os
from typing import Dict, List

# Project imports
from src.crypto import decrypt, encrypt
from src.sigma_interface.sigma_client import SigmaClient
from src.utils import Update, Op, AddToken, SrchToken
from src.zhao_nishide.zn_client import ZNClient


class LibertasClient(object):
    """Libertas client implementation.

    Libertas uses a wildcard supporting SSE scheme internally. In addition to the security guarantees and functionality
    provided by the underlying scheme, Libertas provides Update Pattern Revealing Backward Privacy.
    """

    def __init__(
            self,
            sigma: SigmaClient[AddToken, SrchToken],
    ) -> None:
        """Initializes a Libertas client, setting the underlying client scheme that is used.

        :param sigma: The underlying SSE scheme used by this Libertas instance
        :type sigma: ZNClient
        :returns: None
        :rtype: None
        """
        self.sigma: SigmaClient = sigma
        self.k = None
        self.t = None

    def setup(
            self,
            security_parameter: (int, int) = (256, 2048),
    ) -> None:
        """Sets up the Libertas client, generating a key used for future operations and initializing the scheme's
        timestamp counter.

        :param security_parameter: The required security strength for the AES encryption of Libertas and the security
         strength for the underlying scheme (bits)
        :type security_parameter: (int, int)
        :returns: None
        :rtype: None
        """
        self.sigma.setup(security_parameter[1])
        self.k = os.urandom(security_parameter[0] // 8)
        self.t = 0

    def srch_token(
            self,
            q: str,
    ) -> SrchToken:
        """Creates a search token for a query, to be send to the server.

        :param q: The query, a string of characters, possibly containing wildcards
        :type q: str
        :returns: The search token
        :rtype: SrchToken
        """
        return self.sigma.srch_token(q)

    def add_token(
            self,
            ind: int,
            w: str,
    ) -> AddToken:
        """Creates an add token for a document-keyword pair, to be send to the server.

        :param ind: The document identifier of the document in the document-keyword pair that is to be added
        :type ind: int
        :param w: The keyword in the document-keyword pair that is to be added
        :type w: str
        :returns: the add token
        :rtype: AddToken
        """
        self.t = self.t + 1
        content = self._encrypt_update(self.t, Op.ADD, ind, w)
        return self.sigma.add_token(content, w)

    def del_token(
            self,
            ind: int,
            w: str,
    ) -> AddToken:
        """Creates a delete token for a document-keyword pair, to be send to the server.

        :param ind: The document identifier of the document in the document-keyword pair that is to be deleted
        :type ind: int
        :param w: The keyword in the document-keyword pair that is to be deleted
        :type w: str
        :returns: the delete token
        :rtype: AddToken
        """
        self.t = self.t + 1
        content = self._encrypt_update(self.t, Op.DEL, ind, w)
        return self.sigma.add_token(content, w)

    def dec_search(
            self,
            r_star: List[int],
    ) -> List[int]:
        """Decrypts encrypted updates received from the server and determines which document identifiers are still
        relevant for the query. Document identifiers are relevant when there is a keyword-document pair that is
        added, but not deleted afterwards.

        :param r_star: A list of encrypted updates
        :type r_star: List[int]
        :returns: A list of document identifiers matching with the initial query
        :rtype: List[int]
        """
        # Decrypt r_star and sort it according to timestamp t
        decrypted_updates: List[Update] = list(map(lambda e: self._decrypt_update(e), r_star))
        decrypted_updates.sort(key=lambda x: x[0])

        keyword_documents_dict: Dict[str, List[int]] = {}
        for update in decrypted_updates:
            # Unpack entry (see utils.Update)
            (t, op, ind, w) = update

            if w not in keyword_documents_dict:
                keyword_documents_dict[w] = []

            documents_list: List[int] = keyword_documents_dict[w]
            if op == Op.ADD and ind not in documents_list:
                # Add ind to the results for this keyword
                documents_list.append(ind)
                keyword_documents_dict[w] = documents_list
            elif op == Op.DEL and ind in documents_list:
                # Remove ind from the results for this keyword
                documents_list.remove(ind)
                keyword_documents_dict[w] = documents_list

        # Combine the ind values for all keywords and remove duplicates
        results = [ind for sub_results in keyword_documents_dict.values() for ind in sub_results]
        return list(set(results))

    def _encrypt_update(
            self,
            t: int,
            op: Op,
            ind: int,
            w: str,
    ) -> int:
        """Encrypts a (t, op, ind, w) tuple.

        :param t: The timestamp in the tuple
        :type t: int
        :param op: The operation (add or delete) in the tuple
        :type op: Op
        :param ind: The document identifier in the tuple
        :type ind: int
        :param w: The keyword in the tuple
        :type w: str
        :returns: The tuple in encrypted form
        :rtype: int
        """
        update_str: str = '{0},{1},{2},{3}'.format(t, op.value, ind, w)
        encrypted_update_str: bytes = encrypt(self.k, update_str)
        return int.from_bytes(encrypted_update_str, byteorder='big')

    def _decrypt_update(
            self,
            cipher_text: int,
    ) -> Update:
        """Decrypts the encryption of a (t, op, ind, w) tuple.

        :param cipher_text: The encrypted tuple
        :type cipher_text: int
        :returns: The (t, op, ind, w) tuple
        :rtype: Update
        """
        # Ensure byte alignment of 16 because of CBC mode
        byte_length = math.ceil(math.log(cipher_text, 2) / 8 / 16) * 16
        cipher_text_bytes: bytes = int.to_bytes(cipher_text, byteorder='big', length=byte_length)
        update_str: str = decrypt(self.k, cipher_text_bytes)
        (t, op, ind, w) = update_str.split(',')
        return int(t), Op(int(op)), int(ind), w
