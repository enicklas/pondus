# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2007-09  Eike Nicklas <eike@ephys.de>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from datetime import date

from pondus.core import xml_parser
from pondus.core.dataset import Dataset


class AllDatasets(object):
    """Defines the structure how all the datasets are stored
    internally."""

    def __init__(self, datasets):
        self.datasets = datasets

    def __iter__(self):
        """Iterates over the datasets."""
        return self.datasets.itervalues()

    def __len__(self):
        """Returns the number of datasets in self.datasets."""
        return len(self.datasets)

    def add(self, dataset):
        """Adds a given dataset object to the datasets or updates, if
        the id already exists."""
        self.datasets[dataset.id] = dataset

    def remove(self, id_):
        """Removes the dataset with the given id from the
        datasets."""
        del self.datasets[id_]

    def get(self, id_):
        """Returns the dataset with the given id."""
        return self.datasets[id_]

    def get_new_dataset(self):
        """Returns a new dataset initialized with today's date and the
        last measured weight."""
        id_ = self.get_new_id()
        date_ = date.today()
        weight = self._last_measured_weight()
        return Dataset(id_, date_, weight)

    def get_new_id(self):
        """Returns an unused id."""
        try:
            return max(self.datasets) + 1
        except ValueError:
            # no datasets exist
            return 1

    def _last_measured_weight(self):
        """Returns the last measured weight."""
        if self.datasets:
            # create an intermediate list of tuples (date, id)
            intermed = [(dataset.get('date'), id_) \
                for id_, dataset in self.datasets.iteritems()]
            # find id of most recent dataset and get its weight value
            return self.datasets[max(intermed)[1]].get('weight')
        else:
            return 0.0


class AllDatasetsOld(AllDatasets):
    """Defines the structure how all the datasets are stored
    internally. Subclass to support the legacy xml scheme."""

    def __init__(self, filepath):
        """Reads all datasets from filepath."""
        self.datasets = xml_parser.read_old(filepath)
