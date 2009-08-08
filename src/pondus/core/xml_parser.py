# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2007-09  Eike Nicklas <eike@ephys.de>

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

from pondus import parameters
from pondus.core import util
from pondus.core.dataset import Dataset

try:
    from xml.etree.cElementTree import parse
except ImportError:
    from elementtree.ElementTree import parse


def read_old(filepath):
    """Parses the legacy xml-file in filepath and returns a dictionary
    containing the datasets."""
    datasets = {}
    if os.path.isfile(filepath):
        user_tree = parse(filepath)
        dataset_list = user_tree.findall('dataset')
        if parameters.convert_weight_data_to_kg == True:
            for dataset_el in dataset_list:
                _add_dataset_to_dict_convert(dataset_el, datasets)
        else:
            for dataset_el in dataset_list:
                _add_dataset_to_dict(dataset_el, datasets)
    return datasets

def read(filepath):
    """Parses the xml-file in filepath and returns the data necessary to
    create a person object."""
    person_data = {}
    person_data['height'] = 0.0
    person_data['measurements'] = {}
    person_data['plan'] = {}
    if os.path.isfile(filepath):
        user_tree = parse(filepath)
        height_element = user_tree.find('height')
        if height_element is not None:
            person_data['height'] = float(height_element.text)
        measurements = user_tree.findall('weight/measurements/dataset')
        plan = user_tree.findall('weight/plan/dataset')
        for dataset_el in measurements:
            _add_dataset_to_dict(dataset_el, person_data['measurements'])
        for dataset_el in plan:
            _add_dataset_to_dict(dataset_el, person_data['plan'])
    return person_data

def _add_dataset_to_dict(dataset_el, datasets):
    """Adds a dataset element to a dictionary of Dataset objects."""
    dataset = Dataset(int(dataset_el.get('id')), \
                      util.str2date(dataset_el.find('date').text), \
                      float(dataset_el.find('weight').text))
    datasets[int(dataset_el.get('id'))] = dataset

def _add_dataset_to_dict_convert(dataset_el, datasets):
    """Adds a dataset element to a dictionary of Dataset objects and
    converts the weight from lbs to kg."""
    weight = float(dataset_el.find('weight').text)
    weight = round(util.lbs_to_kg(weight), 2)
    dataset = Dataset(int(dataset_el.get('id')), \
                      util.str2date(dataset_el.find('date').text), \
                      weight)
    datasets[int(dataset_el.get('id'))] = dataset
