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

def kg_to_lbs(weight):
    """Converts the weight in kg to lbs."""
    return weight/0.45359237

def lbs_to_kg(weight):
    """Converts the weight in lbs to kg."""
    return weight*0.45359237

def get_weight_unit():
    """Returns the weight unit preferred by the user."""
    if parameters.config['preferences.unit_system'] == 'metric':
        return _('kg')
    elif parameters.config['preferences.unit_system'] == 'imperial':
        return _('lbs')

def height_to_metric(height):
    """Converts height in cm to m/cm."""
    meters = int(height) / 100
    cmeters = height % 100
    return meters, cmeters

def height_to_imperial(height):
    """Converts height in cm to feet/inches."""
    height_inches = height / 2.54
    feet = int(height_inches) / 12
    inches = height_inches % 12
    return feet, inches

def metric_to_height(meters, cmeters):
    """Converts height in m/cm to cm."""
    return 100*meters + cmeters

def imperial_to_height(feet, inches):
    """Converts height in feet/inches to cm."""
    return 2.54*(12*feet + inches)
