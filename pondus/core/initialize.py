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

from pondus.core import parameters
from pondus.core import config_parser
from pondus.core import option_parser
from pondus.core.logger import logger
from pondus.core.filelock import FileLock
from pondus.core.person import Person


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
        logger.error(_('Could not find %s'), sysfilepath)
        sys.exit(1)


def _test_gtk_availability():
    """Tests availability of pygtk and quits if not found."""
    try:
        import gtk
    except ImportError:
        logger.error(_('Please make sure pygtk is installed.'))
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
    check_datadir(parameters.userdatafile)
    parameters.filelock = FileLock()
    parameters.plot_button_path = _get_path(
            'data/icons/', '../share/pondus/', 'plot.png')
    parameters.logo_path = _get_path(
            'data/icons/', '../share/icons/hicolor/48x48/apps/', 'pondus.png')
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
