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

from datetime import date
from time import strptime

from pondus import parameters

def str2date(datestring):
    """Converts a string in the format YYYY-MM-DD into a date object."""
    return date(*strptime(datestring, '%Y-%m-%d')[0:3])

def compare_with_possible_nones(min1, max1, min2, max2):
    """Compares min1 with min2 and max max1 with max2 and returns the
    total minimum and maximum. min1 and min2 can possibly be None; it is
    assumed, that max1 and max2 then are also None."""
    if min1 is not None and min2 is not None:
        tot_min = min(min1, min2)
        tot_max = max(max1, max2)
        return tot_min, tot_max
    if min1 is not None and min2 is None:
        return min1, max1
    if min1 is None and min2 is not None:
        return min2, max2
    else:
        return None, None

def bmi(weight, height):
    """Returns the body mass index. weight and height should be given
    in metric units, i.e. kg and cm."""
    return weight/(height/100.0)**2

def lbs2kg(weight):
    """Converts the weight in pounds to kg."""
    return weight*0.45359237

def inch2cm(height):
    """Converts the height in feet/inches to cm. height is given as a
    tuple (feet, inches)."""
    inches = 12*height[0] + height[1]
    return inches*2.54

def get_weight_unit():
    """Returns the weight unit preferred by the user."""
    if parameters.config['preferences.unit_system'] == 'metric':
        return _('kg')
    elif parameters.config['preferences.unit_system'] == 'imperial':
        return _('lbs')
    
    