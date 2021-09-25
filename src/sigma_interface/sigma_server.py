# Python imports
from typing import List, Generic

# Project imports
from src.utils import AddToken, SrchToken


class SigmaServer(Generic[AddToken, SrchToken]):
    """Server interface of a wildcard supporting SSE scheme to be used for a Libertas server."""

    def __init__(
            self,
    ) -> None:
        """Initializes a server.

        :returns: None
        :rtype: None
        """
        pass

    def build_index(
            self,
    ) -> None:
        """Sets up the server, initializing its index.

        :returns: None
        :rtype: None
        """
        pass

    def search(
            self,
            srch_token: SrchToken,
    ) -> List[int]:
        """Searches the index for a query represented by a search token and returns matching document identifiers.

        :param srch_token: The search token
        :type srch_token: SrchToken
        :returns: A list of results
        :rtype: List[int]
        """

    def add(
            self,
            add_token: AddToken,
    ) -> None:
        """Adds a document-keyword pair, represented by an add token, to the index.

        :param add_token: An add token representing a document-keyword pair
        :type add_token: AddToken
        :returns: None
        :rtype: None
        """
        pass
