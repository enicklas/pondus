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
            self.height = None
            self.measurements =  AllDatasetsOld(parameters.datafile_old)
            self.plan = AllDatasetsOld(parameters.planfile_old)

    def write_to_file(self, filepath):
        """Writes the person data to the xml file."""
        dom = xml_parser.create_xml_base()
        self.write_to_dom(dom)
        xml_parser.dom2file(dom, filepath)

    def write_to_dom(self, dom):
        """Adds the person data to the given dom."""
        top_element = dom.documentElement
        # write height
        if self.height is not None:
            height = dom.createElement('height')
            height.appendChild(dom.createTextNode(str(self.height)))
            top_element.appendChild(height)
        # write weights
        weights = dom.createElement('weight')
        # write measurements
        measurements = dom.createElement('measurements')
        for dataset in self.measurements:
            newdataset = dom.createElement('dataset')
            newdataset.setAttribute('id', str(dataset.id))
            for parameter, value in dataset.data.iteritems():
                element = dom.createElement(parameter)
                element.appendChild(dom.createTextNode(str(value)))
                newdataset.appendChild(element)
            measurements.appendChild(newdataset)
        weights.appendChild(measurements)
        # write plan
        plan = dom.createElement('plan')
        for dataset in self.plan:
            newdataset = dom.createElement('dataset')
            newdataset.setAttribute('id', str(dataset.id))
            for parameter, value in dataset.data.iteritems():
                element = dom.createElement(parameter)
                element.appendChild(dom.createTextNode(str(value)))
                newdataset.appendChild(element)
            plan.appendChild(newdataset)
        weights.appendChild(plan)
        top_element.appendChild(weights)
