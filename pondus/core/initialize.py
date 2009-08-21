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

import gettext
import os
import sys

from pondus import parameters
from pondus.core import config_parser
from pondus.core import option_parser
from pondus.core.filelock import FileLock


def _gettext_install():
    """Installs string translations; uses local data if available."""
    basepath = os.path.abspath(sys.path[0])
    if os.path.exists(os.path.join(basepath, 'po/mo')):
        gettext.install('pondus', os.path.join(basepath, 'po/mo'))
    else:
        gettext.install('pondus', os.path.join(basepath, '../share/locale'))

def _get_path(localpath, syspath, filename):
    """Returns the full path to the file with filename. If it exists,
    localpath is used, otherwise the corresponding system directory."""
    basepath = os.path.abspath(sys.path[0])
    localfilepath = os.path.join(basepath, localpath, filename)
    if os.path.exists(localfilepath):
        return localfilepath
    sysfilepath = os.path.join(basepath, syspath, filename)
    if os.path.exists(sysfilepath):
        return sysfilepath
    else:
        print _('Error: Could not find'), sysfilepath

def _test_mpl_availability():
    """Tests availability of matplotlib to decide whether plotting
    should be enlabled."""
    try:
        from matplotlib import dates
    except ImportError:
        print _('Note: python-matplotlib is not installed, plotting disabled!')
        return False
    else:
        return True

def _test_gtk_availability():
    """Tests availability of pygtk and quits if not found."""
    try:
        import gtk
    except ImportError, strerror:
        print strerror
        print _('Please make sure this library is installed.')
        sys.exit(1)

def _test_etree_availability():
    """Tests availability of ElementTree and quits if not found."""
    try:
        from xml.etree.cElementTree import parse
    except ImportError:
        try:
            from elementtree.ElementTree import parse
        except ImportError:
            print _('Please make sure ElementTree is installed.')
            sys.exit(1)

def check_datadir(filepath):
    """Checks, whether the directory containing the user data exists
    and creates it if necessary."""
    if not os.path.exists(filepath):
        dirpath = os.path.dirname(filepath)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

def initialize():
    """Initializes the main program with the non-default values and checks
    availability of dependencies."""
    _gettext_install()
    option_parser.parse_options()
    _test_gtk_availability()
    _test_etree_availability()
    check_datadir(parameters.userdatafile)
    parameters.filelock = FileLock()
    parameters.have_mpl = _test_mpl_availability()
    parameters.plot_button_path = _get_path('data/icons/', \
                        '../share/pondus/', 'plot.png')
    parameters.logo_path = _get_path('data/icons/', \
                        '../share/icons/hicolor/48x48/apps/', 'pondus.png')
    parameters.config = config_parser.read_config( \
                    parameters.config_default, parameters.configfile)
