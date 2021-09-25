# Python imports
import timeit

# Third-party imports
from typing import List, Tuple

# Project imports
from libertas.libertas_client import LibertasClient
from libertas.libertas_server import LibertasServer
from zhao_nishide.zn_client import ZNClient
from zhao_nishide.zn_server import ZNServer

"""
Evaluation parameters
"""
SEED_VALUE = 314

INSTANCES = 10  # Number of scheme instances. Different instances use different keys
QUERIES = 10  # Number of queries to run for an instance of a scheme
ITERATIONS = 1  # Number of iterations of one query on one instance of a scheme

MAX_DATA_SIZE = 100000
KEYWORD_LENGTH = 5
ZN_FP_RATE = .01
ZN_KEY_LENGTH = 2048
LIBERTAS_KEY_LENGTH = 256


def generate_data(
        data_size: int,
) -> List[Tuple[int, str]]:
    """Generates at most 100,000 document-keyword pairs in the form [(0, '00000'), (1, '00001'), ..., (99999, '99999')].

    :param data_size: The number of document-keyword pairs to be generated
    :type data_size: int
    :returns: List[Tuple[int, str]]
    :rtype: A specified number of document-keyword pairs
    """
    if data_size > MAX_DATA_SIZE:
        raise AssertionError('Provided data size exceeds maximum')
    return [(n, str(n).zfill(KEYWORD_LENGTH)) for n in range(data_size)]


def prepare_schemes(
        data_set: List[Tuple[int, str]],
) -> (ZNClient, ZNServer, LibertasClient, LibertasServer):
    client_zn = ZNClient(ZN_FP_RATE, KEYWORD_LENGTH)
    client_zn.setup(ZN_KEY_LENGTH)
    server_zn = ZNServer()
    server_zn.build_index()

    client_lib = LibertasClient(ZNClient(ZN_FP_RATE, KEYWORD_LENGTH))
    client_lib.setup((LIBERTAS_KEY_LENGTH, ZN_KEY_LENGTH))
    # Set the key of the underlying ZN scheme to be the same as the ZN scheme. As the key greatly influences the
    # search time due to the nature of the search operation, we require them to be equal for a fair performance
    # comparison.
    client_lib.sigma.k = client_zn.k
    server_lib = LibertasServer(ZNServer())
    server_lib.build_index()

    for (ind, w) in data_set:
        add_token = client_zn.add_token(ind, w)
        server_zn.add(add_token)

        add_token = client_lib.add_token(ind, w)
        server_lib.add(add_token)

    return client_zn, server_zn, client_lib, server_lib


def measure_zn(
        zn_client: ZNClient,
        zn_server: ZNServer,
        query: str,
) -> float:
    def time_zn(
            server: ZNServer,
            search_token: Tuple[List[int], List[bytes]],
    ) -> None:
        server.search(search_token)

    srch_token = zn_client.srch_token(query)
    t = timeit.Timer(lambda: time_zn(zn_server, srch_token))
    return t.timeit(ITERATIONS) / ITERATIONS


def measure_libertas(
        lib_client: LibertasClient,
        lib_server: LibertasServer,
        query: str,
) -> float:
    def time_lib(
            client: LibertasClient,
            server: LibertasServer,
            search_token: Tuple[List[int], List[bytes]],
    ) -> None:
        encrypted_results = server.search(search_token)
        client.dec_search(encrypted_results)

    srch_token = lib_client.srch_token(query)
    t = timeit.Timer(lambda: time_lib(lib_client, lib_server, srch_token))
    return t.timeit(ITERATIONS) / ITERATIONS
