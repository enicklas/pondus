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

class Dataset(object):
    """Implements the structure of single weight measurements."""

    def __init__(self, id_, date, weight):
        """Creates a new dataset with the given values."""
        self.data = {}
        self.id =  id_
        self.data['date'] = date
        self.data['weight'] = weight

    def get(self, key):
        """Returns the value of the dataset corresponding to key or
        an empty string."""
        return self.data.get(key, '')

    def set(self, key, value):
        """Sets the property corresponding to key to value."""
        self.data[key] = value

    def as_list(self):
        """Returns the values of a dataset as a list."""
        return [self.id] + self.data.values()

    def as_string_list(self):
        """Returns the values of the dataset as a list of strings."""
        return [str(value) for value in self.data.itervalues()]
