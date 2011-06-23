# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2011 Eike Nicklas <eike@ephys.de>

This program is free software licensed under the MIT license. For details
see LICENSE or http://www.opensource.org/licenses/mit-license.php
"""

import os
from xml.etree.cElementTree import Element, SubElement, ElementTree, parse

from pondus.core import util
from pondus.core.dataset import Dataset


class SportstrackerBackend(object):
    """Backend to read and write AllDatasets data to Sportstracker format."""

    default_filename = os.path.join(os.path.expanduser('~'),
                            '.sportstracker', 'weights.xml')
    fileending = 'xml'

    def write(self, data, filename):
        """Creates a sportstracker weights file at filename containing the
        data; data is an AllDatasets instance."""
        id_ = 1
        weightlist_el = Element('weight-list')
        for dataset in data:
            weight_el = SubElement(weightlist_el, 'weight')
            id_el = SubElement(weight_el, 'id')
            id_el.text = str(id_)
            date_el = SubElement(weight_el, 'date')
            date_el.text = str(dataset.date) + 'T12:00:00'
            value_el = SubElement(weight_el, 'value')
            value_el.text = str(dataset.weight)
            comment_el = SubElement(weight_el, 'comment')
            comment_el.text = dataset.note
            id_ += 1
        st_tree = ElementTree(weightlist_el)
        st_tree.write(filename, encoding='UTF-8')

    def read(self, filename):
        """Reads the sportstracker weights file at filename and returns a
        list of datasets."""
        st_tree = parse(filename)
        datasets = []
        id_ = 1
        st_datasets = st_tree.findall('weight')
        for st_dataset in st_datasets:
            date = util.str2date(st_dataset.find('date').text[0:10])
            weight = round(float(st_dataset.find('value').text), 1)
            note = st_dataset.find('comment').text
            datasets.append(Dataset(id_, date, weight, note=note))
            id_ += 1
        return datasets
