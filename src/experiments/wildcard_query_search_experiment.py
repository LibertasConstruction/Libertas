# Python imports
import math
import random
import time

# Project imports
from experiments.experiment_utils import generate_data, KEYWORD_LENGTH, SEED_VALUE, INSTANCES, QUERIES, \
    prepare_schemes, measure_zn, measure_libertas


class WildcardQuerySearchExperiment:
    def __init__(
            self,
    ) -> None:
        print('--- Wildcard query search experiment ---')
        random.seed(SEED_VALUE)
        start_time = time.process_time()

        index_size = 10000
        data_set = generate_data(index_size)

        matching_keywords_array = [1, 10, 100, 1000, 10000]
        for matching_keywords in matching_keywords_array:
            print('Running measurements for', matching_keywords, 'matching',
                  'keyword' if matching_keywords == 1 else 'keywords')

            number_of_wildcards = int(math.log10(matching_keywords))
            search_times_zn = []
            search_times_lib = []

            for instance_number in range(INSTANCES):
                print('Running instance', instance_number)
                (client_zn, server_zn, client_lib, server_lib) = prepare_schemes(data_set)

                queries = [str(random.randint(0, index_size - 1)).zfill(KEYWORD_LENGTH) for _ in range(QUERIES)]
                queries = map(lambda q: q[:KEYWORD_LENGTH - number_of_wildcards] + '_' * number_of_wildcards, queries)

                for query in queries:
                    search_times_zn.append(measure_zn(client_zn, server_zn, query))
                    search_times_lib.append(measure_libertas(client_lib, server_lib, query))

                print('Taking', time.process_time() - start_time, 'seconds')

            print('ZN:      ', list(map(lambda t: '{:.3f}'.format(t), search_times_zn)))
            print('Libertas:', list(map(lambda t: '{:.3f}'.format(t), search_times_lib)))

            print('ZN   avg.:', sum(search_times_zn) / len(search_times_zn))
            print('Lib. avg.:', sum(search_times_lib) / len(search_times_lib))
