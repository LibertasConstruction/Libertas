# Python imports
import random
import time

# Project imports
from experiments.experiment_utils import generate_data, KEYWORD_LENGTH, SEED_VALUE, INSTANCES, QUERIES, \
    prepare_schemes, measure_libertas, measure_zn


class DeletionExperiment:
    def __init__(
            self,
    ) -> None:
        print('--- Deletion experiment ---')
        random.seed(SEED_VALUE)
        start_time = time.process_time()

        index_size = 10000
        deletions_array = range(0, index_size + index_size // 10, index_size // 10)
        data_set = generate_data(index_size)

        search_times_zn = []
        search_times_lib = []

        for instance_number in range(INSTANCES):
            print('Running instance', instance_number)

            (client_zn, server_zn, client_lib, server_lib) = prepare_schemes(data_set)

            queries = [str(random.randint(0, index_size - 1)).zfill(KEYWORD_LENGTH) for _ in range(QUERIES)]

            search_times_zn_deletions = []
            search_times_lib_deletions = []

            for deletions in deletions_array:
                print('Running measurements for', deletions, 'deletions')

                search_times_zn_queries = []
                search_times_lib_queries = []

                for (ind, w) in data_set[0 if deletions == 0 else deletions - index_size // 10:deletions]:
                    del_token = client_zn.del_token(ind, w)
                    server_zn.delete(del_token)
                    del_token = client_lib.del_token(ind, w)
                    server_lib.delete(del_token)

                for query in queries:
                    search_times_zn_queries.append(measure_zn(client_zn, server_zn, query))
                    search_times_lib_queries.append(measure_libertas(client_lib, server_lib, query))

                search_times_zn_deletions.append(sum(search_times_zn_queries) / len(search_times_zn_queries))
                search_times_lib_deletions.append(sum(search_times_lib_queries) / len(search_times_lib_queries))

                print('Taking', time.process_time() - start_time, 'seconds')

            search_times_zn.append(search_times_zn_deletions)
            search_times_lib.append(search_times_lib_deletions)

        print('ZN   avg.:', list(map(lambda item: sum(item) / len(item), zip(*search_times_zn))))
        print('Lib. avg.:', list(map(lambda item: sum(item) / len(item), zip(*search_times_lib))))
