# Python imports
import random
import time

# Project imports
from experiments.experiment_utils import generate_data, KEYWORD_LENGTH, SEED_VALUE, INSTANCES, QUERIES, \
    prepare_schemes, measure_libertas, measure_zn


class MultipleResultsExperiment:
    def __init__(
            self,
    ) -> None:
        print('--- Multiple results experiment ---')
        random.seed(SEED_VALUE)
        start_time = time.process_time()

        index_size = 10000

        matching_documents_array = [1, 10, 100, 1000, 10000]
        for matching_documents in matching_documents_array:
            print('Running measurements for', matching_documents, 'matching',
                  'document' if matching_documents == 1 else 'documents')

            irrelevant_item_size = index_size - matching_documents
            data_set = generate_data(irrelevant_item_size)
            keyword = str(irrelevant_item_size).zfill(KEYWORD_LENGTH)
            results = [(n + irrelevant_item_size, keyword) for n in range(matching_documents)]
            data_set = data_set + results

            search_times_zn = []
            search_times_lib = []

            for instance_number in range(INSTANCES):
                print('Running instance', instance_number)
                (client_zn, server_zn, client_lib, server_lib) = prepare_schemes(data_set)
                for _ in range(QUERIES):
                    search_times_zn.append(measure_zn(client_zn, server_zn, keyword))
                    search_times_lib.append(measure_libertas(client_lib, server_lib, keyword))

                print('Taking', time.process_time() - start_time, 'seconds')

            print('ZN:      ', list(map(lambda t: '{:.3f}'.format(t), search_times_zn)))
            print('Libertas:', list(map(lambda t: '{:.3f}'.format(t), search_times_lib)))

            print('ZN   avg.:', sum(search_times_zn) / len(search_times_zn))
            print('Lib. avg.:', sum(search_times_lib) / len(search_times_lib))
