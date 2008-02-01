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
import sys

def local_or_sys(localpath, syspath):
    """Returns the requested localpath relative to the project
    directory, if it exists, and the corresponding system directory
    otherwise."""
    localpath = sys.path[0] + '/../' + localpath
    if os.path.isdir(localpath):
        return localpath
    else:
        return sys.prefix + '/' + syspath

# path of the xml file to use
datafile = os.path.expanduser('~/.pondus/datasets.xml')

# tags used in the xml file
rootnametag = 'dataset-list'
datasettag = 'dataset'
datetag = 'date'
weighttag = 'weight'

# paths to button/logo icons used
button_base_dir = local_or_sys('data/icons/', 'share/pondus/')
plot_button_path = button_base_dir + 'plot.png'

logo_base_dir = local_or_sys('data/icons/', 'share/icons/hicolor/48x48/apps/')
logo_path = logo_base_dir + 'pondus.png'
