# Project imports
from experiments.deletion_experiment import DeletionExperiment
from experiments.exact_keyword_search_experiment import ExactKeywordSearchExperiment
from experiments.multiple_results_experiment import MultipleResultsExperiment
from experiments.wildcard_query_search_experiment import WildcardQuerySearchExperiment

if __name__ == '__main__':
    ExactKeywordSearchExperiment()
    WildcardQuerySearchExperiment()
    DeletionExperiment()
    MultipleResultsExperiment()
