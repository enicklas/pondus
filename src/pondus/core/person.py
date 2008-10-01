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

import os

from pondus.core import xml_parser
from pondus.core.all_datasets import AllDatasets, AllDatasetsOld
from pondus import parameters

try:
    from xml.etree.cElementTree import Element, SubElement, ElementTree
except ImportError:
    from elementtree.ElementTree import Element, SubElement, ElementTree


class Person(object):
    """Implements the structure to store the user data."""

    def __init__(self, filepath):
        """Creates a new person object from the xml file at filepath."""
        if os.path.isfile(filepath) or parameters.use_custom_file \
                or not os.path.isfile(parameters.datafile_old):
            person_data = xml_parser.read(filepath)
            self.height = person_data['height']
            self.measurements = AllDatasets(person_data['measurements'])
            self.plan = AllDatasets(person_data['plan'])
        else:
            self.height = 0.0
            self.measurements =  AllDatasetsOld(parameters.datafile_old)
            self.plan = AllDatasetsOld(parameters.planfile_old)

    def write_to_file(self, filepath):
        """Writes the person data to the xml file."""
        person_el = Element('person')
        height_el = SubElement(person_el, 'height')
        height_el.text = str(self.height)
        weight_el = SubElement(person_el, 'weight')
        measurements_el = SubElement(weight_el, 'measurements')
        plan_el = SubElement(weight_el, 'plan')
        for dataset in self.measurements:
            self.__add_dataset_to_element(dataset, measurements_el)
        for dataset in self.plan:
            self.__add_dataset_to_element(dataset, plan_el)
        user_tree = ElementTree(person_el)
        user_tree.write(filepath, encoding='UTF-8')

    def __add_dataset_to_element(self, dataset, element):
        """Adds a dataset object to an element, which is the parent in
        the ElementTree."""
        dataset_el = SubElement(element, 'dataset')
        dataset_el.set('id', str(dataset.id))
        for parameter, value in dataset.data.iteritems():
            sub_el = SubElement(dataset_el, parameter)
            sub_el.text = str(value)
