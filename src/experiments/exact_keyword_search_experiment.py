# Python imports
import random
import time

# Project imports
from experiments.experiment_utils import generate_data, KEYWORD_LENGTH, SEED_VALUE, INSTANCES, QUERIES, \
    prepare_schemes, measure_zn, measure_libertas


class ExactKeywordSearchExperiment:
    def __init__(
            self,
    ) -> None:
        print('--- Exact keyword search experiment ---')
        random.seed(SEED_VALUE)
        start_time = time.process_time()

        index_sizes = [100, 1000, 10000, 100000]
        for index_size in index_sizes:
            print('Running measurements for index size', index_size)

            data_set = generate_data(index_size)

            search_times_zn = []
            search_times_lib = []

            for instance_number in range(INSTANCES):
                print('Running instance', instance_number)
                (client_zn, server_zn, client_lib, server_lib) = prepare_schemes(data_set)

                queries = [str(random.randint(0, index_size - 1)).zfill(KEYWORD_LENGTH) for _ in range(QUERIES)]
                for query in queries:
                    search_times_zn.append(measure_zn(client_zn, server_zn, query))
                    search_times_lib.append(measure_libertas(client_lib, server_lib, query))

                print('Taking', time.process_time() - start_time, 'seconds')

            print('ZN:      ', list(map(lambda t: '{:.3f}'.format(t), search_times_zn)))
            print('Libertas:', list(map(lambda t: '{:.3f}'.format(t), search_times_lib)))

            print('ZN   avg.:', sum(search_times_zn) / len(search_times_zn))
            print('Lib. avg.:', sum(search_times_lib) / len(search_times_lib))
