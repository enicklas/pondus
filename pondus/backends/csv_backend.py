# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2008-11  Eike Nicklas <eike@ephys.de>

This program is free software licensed under the MIT license. For details
see LICENSE or http://www.opensource.org/licenses/mit-license.php
"""

import csv
import os

from pondus.core import parameters
from pondus.core import util
from pondus.core.dataset import Dataset


class CsvBackend(object):
    """Backend to read and write AllDataset data to a csv file."""

    default_filename = os.path.join(os.path.expanduser('~'), _('weight.csv'))

    def write(self, data, filename):
        """Creates a csv-file at filename containing data."""
        csvfile = open(filename, 'w')
        csvwriter = csv.writer(csvfile)
        if parameters.config['preferences.unit_system'] == 'imperial':
            weight_key = 'weight_lbs'
        else:
            weight_key = 'weight'
        for dataset in data:
            csvwriter.writerow([str(dataset.date),
                                str(round(getattr(dataset, weight_key), 1))])
        csvfile.close()

    def read(self, filename):
        """Reads the csv-file at filename and returns a list of datasets."""
        csvfile = open(filename, 'r')
        csvreader = csv.reader(csvfile)
        datasets = []
        id_ = 1
        # try to read the datasets from the csv file
        try:
            for row in csvreader:
                date = util.str2date(row[0])
                weight = round(float(row[1]), 1)
                dataset = Dataset(id_, date, weight)
                if parameters.config['preferences.unit_system'] == 'imperial':
                    dataset.weight_lbs = weight
                datasets.append(dataset)
                id_ += 1
        except:
            return False
        return datasets
