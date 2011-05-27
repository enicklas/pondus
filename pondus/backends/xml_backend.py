# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2007-11  Eike Nicklas <eike@ephys.de>

This program is free software licensed under the MIT license. For details
see LICENSE or http://www.opensource.org/licenses/mit-license.php
"""

import os
from xml.etree.cElementTree import Element, SubElement, ElementTree, parse

from pondus.core import parameters
from pondus.core import util
from pondus.core.dataset import Dataset
from pondus.core.person import Person


class XmlBackend(object):
    """Backend to read and write Person data from/to an xml file."""

    default_filename = os.path.join(
            os.path.expanduser('~'), '.pondus', 'user_data.xml')

    def write(self, data, filename):
        """Writes data to the xml file. Data is a Person instance."""
        person_el = Element('person', format='0.7')
        height_el = SubElement(person_el, 'height')
        height_el.text = str(data.height)
        weight_el = SubElement(person_el, 'weight')
        measurements_el = SubElement(weight_el, 'measurements')
        plan_el = SubElement(weight_el, 'plan')
        for dataset in data.measurements:
            _add_dataset_to_element(dataset, measurements_el)
        for dataset in data.plan:
            _add_dataset_to_element(dataset, plan_el)
        user_tree = ElementTree(person_el)
        user_tree.write(filename, encoding='UTF-8')

    def read(self, filename):
        """Parses the xml-file in filename and returns a person object."""
        person = Person()
        user_tree = parse(filename)
        height_element = user_tree.find('height')
        if height_element is not None:
            person.height = float(height_element.text)
        measurements = user_tree.findall('weight/measurements/dataset')
        plan = user_tree.findall('weight/plan/dataset')
        for dataset_el in measurements:
            person.measurements.add(_get_dataset_from_element(dataset_el))
        for dataset_el in plan:
            person.plan.add(_get_dataset_from_element(dataset_el))
        return person


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


def _get_dataset_from_element(dataset_el):
    """Parses a dataset xml-element and returns it as a Dataset object."""
    dataset = Dataset(int(dataset_el.find('id').text),
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
