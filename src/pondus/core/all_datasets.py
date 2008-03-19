#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2007-08  Eike Nicklas <eike@ephys.de>

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

    def __init__(self, filepath):
        """Reads all datasets from filepath."""
        self.datasets = xml_parser.read(filepath)

    def __iter__(self):
        """Iterates over the datasets."""
        return self.datasets.itervalues()

    def __len__(self):
        """Returns the number of datasets in self.datasets."""
        return len(self.datasets)

    def write_to_file(self, filepath):
        """Writes all datasets to filepath."""
        xml_parser.write(self.datasets.itervalues(), filepath)

    def add(self, newdataset):
        """Adds a given dataset object to the datasets or updates, if
        the id already exists."""
        self.datasets[newdataset.id] = newdataset

    def remove(self, given_id):
        """Removes the dataset with the given id from the
        datasets."""
        del self.datasets[given_id]

    def get(self, given_id):
        """Returns the dataset with the given id."""
        return self.datasets[given_id]

    def get_new_dataset(self):
        """Returns a new dataset initialized with today's date and the
        last measured weight."""
        new_id = self._get_new_id()
        new_date = date.today()
        new_weight = self._last_measured_weight()
        return Dataset(new_id, new_date, new_weight)

    def _last_measured_weight(self):
        """Returns the last measured weight."""
        if self.datasets != {}:
            intermed = [(dataset.data['date'], idd) \
                for idd, dataset in self.datasets.iteritems()]
            return self.datasets[max(intermed)[1]].data['weight']
        else:
            return ""

    def _get_new_id(self):
        """Returns an unused id."""
        try:
            return max(self.datasets) + 1
        except ValueError:
            #if no datasets exist
            return 1

    def get_daterange(self):
        """Returns the minimum and the maximum date in the available
        datasets. Returns None, None if no measurements exist."""
        try:
            mindate = min(dataset.data['date'] \
                for dataset in self.datasets.itervalues())
            maxdate = max(dataset.data['date'] \
                for dataset in self.datasets.itervalues())
        except ValueError:
            return None, None
        return mindate, maxdate

    def get_weight_in_daterange(self, mindate, maxdate):
        """Returns the minimum and the maximum weight measured in the
        given date range. Returns None, None if no measurements exist
        in the given date range."""
        try:
            minweight = min(dataset.data['weight'] \
                for dataset in self.datasets.itervalues() \
                if mindate <= dataset.data['date'] <= maxdate)
            maxweight = max(dataset.data['weight'] \
                for dataset in self.datasets.itervalues() \
                if mindate <= dataset.data['date'] <= maxdate)
        except ValueError:
            return None, None
        return minweight, maxweight
