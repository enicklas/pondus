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

from pondus import parameters


class Dataset(object):
    """Implements the structure of single weight measurements."""

    def __init__(self, myid, date, weight):
        """Creates a new dataset with the given values."""
        self.data = {}
        self.id =  myid
        self.data['date'] = date
        self.data['weight'] = weight

    def as_list(self):
        """Returns the data of a dataset as a list."""
        return [self.id] + self.data.values()

    def write_to_dom(self, dom):
        """Adds the dataset to the given dom."""
        top_element = dom.documentElement
        newdataset = dom.createElement(parameters.datasettag)
        newdataset.setAttribute('id', str(self.id))
        for parameter, value in self.data.iteritems():
            # create parameter tag
            element = dom.createElement(parameter)
            # create textual content
            element.appendChild(dom.createTextNode(str(value)))
            newdataset.appendChild(element)
        top_element.appendChild(newdataset)
