# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2007-11  Eike Nicklas <eike@ephys.de>

This program is free software licensed under the MIT license. For details
see LICENSE or http://www.opensource.org/licenses/mit-license.php
"""

import os
from optparse import OptionParser

from pondus import __version__
from pondus.core import parameters
from pondus.core.logger import logger


def parse_options():
    """Parses the command line options and performs the corresponding
    actions."""
    parser = OptionParser(version='%prog ' + __version__)
    parser.add_option('-i', '--input',
        dest='filename',
        help='read data from FILE instead of the standard location',
        metavar='FILE')
    (options, args) = parser.parse_args()
    if options.filename:
        _set_datafilepath(options.filename)


def _set_datafilepath(filepath):
    """Updates the path to the file containing the weight data."""
    filepath = os.path.expanduser(filepath)
    if not os.path.isabs(filepath):
        filepath = os.path.join(os.getcwd(), filepath)
    if not os.path.isdir(filepath):
        logger.info(_('Reading file %s'), filepath)
        parameters.userdatafile = filepath
        parameters.use_custom_file = True
        return
    else:
        logger.warning(_('You passed a directory, not a file!'))
        logger.warning( \
                _('Using the standard file ~/.pondus/user_data.xml instead.'))
