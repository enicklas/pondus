#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2008  Eike Nicklas <eike@ephys.de>

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

import csv

from pondus.core import util
from pondus.core.dataset import Dataset

def write_csv(datasetdata, csvfilepath):
    """Creates a csv-file at csvfilepath containing the data from
    datasetdata."""
    csvfile = open(csvfilepath, 'w')
    csvwriter = csv.writer(csvfile)
    for dataset in datasetdata:
        csvwriter.writerow(dataset.value_list())
    csvfile.close()

def read_csv(datasetdata, csvfilepath):
    """Reads the csv-file at csvfilepath and adds the data to
    datasetdata."""
    csvfile = open(csvfilepath, 'r')
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        dataset = datasetdata.get_new_dataset()
        dataset.data['date'] = util.str2date(row[0])
        dataset.data['weight'] = float(row[1])
        datasetdata.add(dataset)
