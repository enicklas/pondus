# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2007-11  Eike Nicklas <eike@ephys.de>

This program is free software licensed under the MIT license. For details
see LICENSE or http://www.opensource.org/licenses/mit-license.php
"""

from datetime import date
from time import strptime

from pondus.core import parameters


def str2date(datestring):
    """Converts a string in the format YYYY-MM-DD into a date object."""
    return date(*strptime(datestring, '%Y-%m-%d')[0:3])


def nonemin(list_):
    """Returns the minimum value in a list ignoring Nones"""
    try:
        return min(element for element in list_ if element is not None)
    except ValueError:
        return None


def nonemax(list_):
    """Returns the maximum value in a list ignoring Nones"""
    try:
        return max(element for element in list_ if element is not None)
    except ValueError:
        return None


def bmi(weight, height):
    """Returns the body mass index. Weight and height should be given
    in kg and cm."""
    return weight / (height / 100.0)**2


def get_weight_unit():
    """Returns the weight unit preferred by the user."""
    if parameters.config['preferences.unit_system'] == 'metric':
        return _('kg')
    elif parameters.config['preferences.unit_system'] == 'imperial':
        return _('lbs')


def height_to_metric(height):
    """Converts height in cm to m/cm."""
    meters = int(height) / 100
    centimeters = height % 100
    return meters, centimeters


def height_to_imperial(height):
    """Converts height in cm to feet/inches."""
    height_inches = height / 2.54
    feet = int(height_inches) / 12
    inches = height_inches % 12
    return feet, inches


def metric_to_height(meters, centimeters):
    """Converts height in m/cm to cm."""
    return 100 * meters + centimeters


def imperial_to_height(feet, inches):
    """Converts height in feet/inches to cm."""
    return 2.54 * (12 * feet + inches)
