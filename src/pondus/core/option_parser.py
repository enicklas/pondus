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
from optparse import OptionParser

from pondus import __version__
from pondus import parameters


def set_datafilepath(filepath):
    filepath = os.path.expanduser(filepath)
    if not os.path.isabs(filepath):
        filepath = os.path.join(os.getcwd(), filepath)
    if not os.path.isdir(filepath):
        print _('Reading file'), filepath
        parameters.datafile = filepath
        return None
    else:
        print _('Error: This is a directory, not a file!')
        print _('Using the standard file ~/.pondus/datasets.xml instead.')

def parse_options():
    parser = OptionParser(version='%prog '+__version__)
    parser.add_option('-i', '--input',
        dest='filename',
        help='read data from FILE instead of the standard location',
        metavar='FILE')
    (options, args) = parser.parse_args()
    if options.filename:
        set_datafilepath(options.filename)
