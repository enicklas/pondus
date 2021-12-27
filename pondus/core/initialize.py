# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2007-11  Eike Nicklas <eike@ephys.de>

This program is free software licensed under the MIT license. For details
see LICENSE or http://www.opensource.org/licenses/mit-license.php
"""

import gettext
import logging
import os
import sys
from importlib import resources

from pondus.core import parameters
from pondus.core import config_parser
from pondus.core import option_parser
from pondus.core.logger import logger
from pondus.core.filelock import FileLock
from pondus.core.person import Person


def _set_paths_and_po():
    """Sets the correct paths to icons and translations depending
    on where the executable is located and which platform is run."""
    basepath = os.path.abspath(sys.path[0])
    with resources.path("pondus.gui.resources", "plot.png") as plot_icon_path:
        parameters.plot_button_path = plot_icon_path.resolve()
    with resources.path("pondus.gui.resources", "pondus.png") as logo_icon_path:
        parameters.logo_path = logo_icon_path.resolve()
    if sys.platform == 'win32':
        # running windows
        gettext.install('pondus', os.path.join(basepath, 'share/locale'))
    elif not basepath.startswith('/usr/'):
        # using local package without installation
        gettext.install('pondus', os.path.join(basepath, 'po/mo'))
    elif basepath.startswith('/usr/local/'):
        # installed to /usr/local/
        gettext.install('pondus', '/usr/local/share/locale')
    else:
        # installed to /usr/, which is default in parameters
        gettext.install('pondus', '/usr/share/locale')


def _test_icon_availability():
    """Checks, whether required icons are available."""
    for filepath in [parameters.plot_button_path, parameters.logo_path]:
        if not os.path.exists(filepath):
            logger.error(_('Could not find %s'), filepath)
            sys.exit(1)


def _test_gtk_availability():
    """Tests availability of PyGObject and quits if not found."""
    try:
        import gi
        gi.require_version('Gtk', '3.0')
        from gi.repository import Gtk
    except ImportError:
        logger.error(_('Please make sure that PyGObject is installed.'))
        sys.exit(1)


def _check_datadir(filepath):
    """Checks, whether the directory containing the user data exists
    and creates it if necessary."""
    if not os.path.exists(filepath):
        dirpath = os.path.dirname(filepath)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)


def initialize():
    """Initializes the main program with the non-default values and checks
    availability of dependencies."""
    _set_paths_and_po()
    option_parser.parse_options()
    _test_icon_availability()
    _test_gtk_availability()
    _check_datadir(parameters.userdatafile)
    parameters.filelock = FileLock()
    parameters.config = config_parser.read_config(
            parameters.config_default, parameters.configfile)
    parameters.user = Person(parameters.userdatafile)


def shutdown():
    """Saves the data to disk."""
    if parameters.filelock.own_lock():
        parameters.user.write_to_file(filepath=parameters.userdatafile)
        config_parser.write_config(parameters.config, parameters.configfile)
        parameters.filelock.unlock()
    else:
        backupfile = parameters.userdatafile + '.backup'
        parameters.user.write_to_file(filepath=backupfile)
        logger.warning(
                _('Not owning the file lock. Backing up the data to %s'),
                backupfile)
    logging.shutdown()
