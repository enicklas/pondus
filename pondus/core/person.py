# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2007-11  Eike Nicklas <eike@ephys.de>

This program is free software licensed under the MIT license. For details
see LICENSE or http://www.opensource.org/licenses/mit-license.php
"""

import os

from pondus.core import parameters
from pondus.core import util
from pondus.core.all_datasets import AllDatasets
from pondus.core.dataset import Dataset

from xml.etree.cElementTree import Element, SubElement, ElementTree, parse


class Person(object):
    """Implements the structure to store the user data."""

    def __init__(self, filepath):
        """Creates a new person object from the xml file at filepath."""
        self.height = 0.0
        self.measurements = AllDatasets({})
        self.plan = AllDatasets({})
        self._read_from_file(filepath)

    def write_to_file(self, filepath):
        """Writes the person data to the xml file."""
        person_el = Element('person', format='0.7')
        height_el = SubElement(person_el, 'height')
        height_el.text = str(self.height)
        weight_el = SubElement(person_el, 'weight')
        measurements_el = SubElement(weight_el, 'measurements')
        plan_el = SubElement(weight_el, 'plan')
        for dataset in self.measurements:
            _add_dataset_to_element(dataset, measurements_el)
        for dataset in self.plan:
            _add_dataset_to_element(dataset, plan_el)
        user_tree = ElementTree(person_el)
        user_tree.write(filepath, encoding='UTF-8')

    def _read_from_file(self, filepath):
        """Parses the xml-file in filepath and adds the data to the
        person object."""
        # if the standard file or the custom file exist, read from it
        if os.path.isfile(filepath):
            user_tree = parse(filepath)
            height_element = user_tree.find('height')
            if height_element is not None:
                self.height = float(height_element.text)
            measurements = user_tree.findall('weight/measurements/dataset')
            plan = user_tree.findall('weight/plan/dataset')
            for dataset_el in measurements:
                self.measurements.add(_dataset_from_element(dataset_el))
            for dataset_el in plan:
                self.plan.add(_dataset_from_element(dataset_el))
            return
        # if using a custom file, that does not exist, start with empty data
        elif parameters.use_custom_file:
            return
        # if none of the above, try to import from the legacy data structure
        elif os.path.isfile(parameters.datafile_old):
            self._read_old_data(parameters.datafile_old, self.measurements)
            self._read_old_data(parameters.planfile_old, self.plan)
            return
        # this is the first start of pondus, start with empty data

    def _read_old_data(self, filepath, datasets):
        """Parses the legacy xml-file in filepath and adds the data to
        datasets."""
        if os.path.isfile(filepath):
            user_tree = parse(filepath)
            dataset_list = user_tree.findall('dataset')
            for dataset_el in dataset_list:
                datasets.add(_dataset_from_element(dataset_el))
        # convert from old units to new standard of always saving weight in kg
        # one-time conversion, performance does not matter
        if parameters.convert_weight_data_to_kg:
            for dataset in datasets:
                dataset.weight_lbs = dataset.weight


def _add_dataset_to_element(dataset, element):
    """Adds a dataset object to an element, which is the parent in
    the ElementTree."""
    dataset_el = SubElement(element, 'dataset')
    for key in parameters.keys_required:
        sub_el = SubElement(dataset_el, key)
        sub_el.text = str(getattr(dataset, key))
    for key in parameters.keys_optional:
        if getattr(dataset, key) is not None:
            sub_el = SubElement(dataset_el, key)
            sub_el.text = str(getattr(dataset, key))


def _dataset_from_element(dataset_el):
    """Parses a dataset xml-element and returns it as a Dataset object."""
    try:
        id_ = int(dataset_el.find('id').text)
    except AttributeError:
        id_ = int(dataset_el.get('id'))
    dataset = Dataset(id_,
                  util.str2date(dataset_el.find('date').text),
                  float(dataset_el.find('weight').text))
    for key in parameters.keys_optional:
        key_el = dataset_el.find(key)
        if key_el is not None:
            if key in ['note']:
                key_data = str(key_el.text)
            else:
                key_data = float(key_el.text)
            setattr(dataset, key, key_data)
    return dataset
