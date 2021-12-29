from pytest import approx

from tests.fixtures.datasets import example_dataset


def test_lbs_property(example_dataset):
    assert example_dataset.weight_lbs == approx(80 / 0.45, rel=1e-2)

    example_dataset.weight_lbs = 200
    assert example_dataset.weight == approx(200 * 0.45, rel=1e-2)
