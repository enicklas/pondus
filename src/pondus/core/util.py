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
from datetime import date
from time import strptime
from xml.dom.minidom import Document

from pondus import parameters
from pondus import __version__


def str2date(datestring):
    """Converts a string in the format YYYY-MM-DD into a date object."""
    return date(*strptime(datestring, '%Y-%m-%d')[0:3])

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

def create_xml_base():
    """Creates a base xml document not containing any datasets."""
    dom = Document()
    roottag = dom.createElement(parameters.rootnametag)
    dom.appendChild(roottag)
    return dom

def dom2file(dom, filepath):
    """Writes dom to file in filepath."""
    f = open(filepath, 'w')
    dom.writexml(f, encoding='UTF-8')
    f.write('\n')
    f.close()

def check_filepath(filepath):
    """Checks whether the file in filepath exists and creates an empty
    base xml document if necessary."""
    if os.path.exists(filepath):
        return None
    else:
        dirpath = os.path.dirname(filepath)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        dom = create_xml_base()
        dom2file(dom, filepath)

def parse_options():
    parser = OptionParser(version='%prog '+__version__)
    parser.add_option("-i", "--input",
        dest="filename",
        help=_("read data from FILE instead of the standard location"),
        metavar=_("FILE"))
    (options, args) = parser.parse_args()
    if options.filename:
        set_datafilepath(options.filename)
