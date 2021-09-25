# Python imports
from typing import Generic

# Project imports
from src.utils import AddToken, SrchToken


class SigmaClient(Generic[AddToken, SrchToken]):
    """Client interface of a wildcard supporting SSE scheme to be used for a Libertas client."""

    def __init__(
            self,
    ) -> None:
        """Initializes the client.

        :returns: None
        :rtype: None
        """
        pass

    def setup(
            self,
            security_parameter: int,
    ) -> None:
        """Sets up the client.

        :param security_parameter: The required security strength (bits)
        :type security_parameter: int
        :returns: None
        :rtype: None
        """
        pass

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
        pass

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
        pass
