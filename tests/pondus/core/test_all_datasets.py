from pytest import approx
from pondus.core.all_datasets import AllDatasets

from tests.fixtures.datasets import example_dataset


def test_all_datasets_init(example_dataset):
    all_datasets = AllDatasets([example_dataset])
    assert len(all_datasets) == 1

    # TODO: Throw error or internally convert to list
    # all_datasets = AllDatasets(example_dataset)
