# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2007-11  Eike Nicklas <eike@ephys.de>

This program is free software licensed under the MIT license. For details
see LICENSE or http://www.opensource.org/licenses/mit-license.php
"""

from datetime import date

from pondus.core.dataset import Dataset


class AllDatasets(object):
    """Defines the structure how all the datasets are stored
    internally. AllDatasets.datasets is a dictionary of Dataset objects
    with their ids as keys."""

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
        """Removes the dataset with the given id from the datasets."""
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
        try:
            # create an intermediate iterator of tuples (date, id)
            intermed = ((dataset.date, id_)
                        for id_, dataset in self.datasets.iteritems())
            # find id of most recent dataset and get its weight value
            return self.datasets[max(intermed)[1]].weight
        except ValueError:
            # no datasets exist
            return 0.0
