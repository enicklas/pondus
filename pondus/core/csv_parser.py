# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2008-11  Eike Nicklas <eike@ephys.de>

This program is free software licensed under the MIT license. For details
see LICENSE or http://www.opensource.org/licenses/mit-license.php
"""

import csv

from pondus.core import parameters
from pondus.core import util
from pondus.core.dataset import Dataset


def write_csv(datasets, csvfilepath):
    """Creates a csv-file at csvfilepath containing the data from
    datasets."""
    csvfile = open(csvfilepath, 'w')
    csvwriter = csv.writer(csvfile)
    if parameters.config['preferences.unit_system'] == 'imperial':
        weight_key = 'weight_lbs'
    else:
        weight_key = 'weight'
    for dataset in datasets:
        csvwriter.writerow([str(dataset.date),
                            str(round(getattr(dataset, weight_key), 1))])
    csvfile.close()


def read_csv(datasets, csvfilepath):
    """Reads the csv-file at csvfilepath and adds the data to
    datasets."""
    csvfile = open(csvfilepath, 'r')
    csvreader = csv.reader(csvfile)
    new_datasets = []
    id_ = datasets.get_new_id()
    # try to read the datasets from the csv file
    try:
        for row in csvreader:
            date = util.str2date(row[0])
            weight = round(float(row[1]), 1)
            dataset = Dataset(id_, date, weight)
            if parameters.config['preferences.unit_system'] == 'imperial':
                dataset.weight_lbs = weight
            new_datasets.append(dataset)
            id_ += 1
    except:
        return False
    # datasets were read successfully, now permanently add them
    for dataset in new_datasets:
        datasets.add(dataset)
    return True
