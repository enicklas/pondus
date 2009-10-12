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
        self.id =  id_
        self.date = date
        self.weight = weight

    def _get_weight_lbs(self):
        return round(self.weight / 0.45359237, 1)
    def _set_weight_lbs(self, new_weight_lbs):
        self.weight = round(new_weight_lbs * 0.45359237, 2)
    weight_lbs = property(_get_weight_lbs, _set_weight_lbs)
