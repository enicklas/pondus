from datetime import date

import pytest

from pondus.core.dataset import Dataset

@pytest.fixture
def example_dataset():
    return Dataset(id_=1, date=date(2021, 12, 29), weight=80)
