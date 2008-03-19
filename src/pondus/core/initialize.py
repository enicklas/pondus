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

from pondus import parameters
from pondus.core import config_parser

def get_path(localpath, syspath, filename):
    """Returns the full path to the file with filename. If it exists,
    localpath is used, otherwise the corresponding system directory."""
    basepath = os.path.dirname(os.path.abspath(sys.path[0]))
    localfilepath = os.path.join(basepath, localpath, filename)
    if os.path.exists(localfilepath):
        return localfilepath
    sysfilepath = os.path.join(basepath, syspath, filename)
    if os.path.exists(sysfilepath):
        return sysfilepath
    else:
        print _('Error: Could not find'), sysfilepath

def test_mpl():
    """Tests availability of matplotlib to decide whether plotting
    should be enlabled."""
    try:
        from matplotlib import dates
        return True
    except ImportError:
        print _('Note: Matplotlib not available, plotting disabled!')
        return False

def initialize():
    """Initializes the main program with the non-default values."""
    parameters.have_mpl = test_mpl()
    parameters.plot_button_path = get_path('data/icons/', \
                        'share/pondus/', 'plot.png')
    parameters.logo_path = get_path('data/icons/', \
                        'share/icons/hicolor/48x48/apps/', 'pondus.png')
    parameters.config = config_parser.read_config( \
                    parameters.config_default, parameters.configfile)
