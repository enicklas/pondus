# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2007-11  Eike Nicklas <eike@ephys.de>

This program is free software licensed under the MIT license. For details
see LICENSE or http://www.opensource.org/licenses/mit-license.php
"""

import os
from xml.etree.cElementTree import parse

from pondus.core import parameters
from pondus.core import util
from pondus.core.dataset import Dataset
from pondus.core.person import Person


class XmlBackendOld(object):
    """Backend to read Person data from an xml file in legacy format."""

    def read(self, meas_filename, plan_filename):
        """Parses the legacy xml-files and returns a Person instance."""
        person = Person()
        meas_datasets = _get_datasets(meas_filename)
        person.measurements.add_list(meas_datasets)
        plan_datasets = _get_datasets(plan_filename)
        person.plan.add_list(plan_datasets)
        return person


def _get_datasets(filename):
    """Parses the legacy xml file at filename and returns
    a list of datasets."""
    datasets = []
    if os.path.isfile(filename):
        user_tree = parse(filename)
        dataset_list = user_tree.findall('dataset')
        for dataset_el in dataset_list:
            dataset = _dataset_from_element(dataset_el)
            if parameters.convert_weight_data_to_kg:
                dataset.weight_lbs = dataset.weight
            datasets.append(dataset)
    return datasets


def _dataset_from_element(dataset_el):
    """Parses a dataset xml-element and returns it as a Dataset object."""
    try:
        id_ = int(dataset_el.find('id').text)
    except AttributeError:
        id_ = int(dataset_el.get('id'))
    dataset = Dataset(id_,
                  util.str2date(dataset_el.find('date').text),
                  float(dataset_el.find('weight').text))
    return dataset
