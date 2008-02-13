#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2008  Eike Nicklas <eike@ephys.de>

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

import os, sys

srcdir = os.path.dirname(os.path.abspath(sys.path[0]))

def get_version():
    """Returns the current version of Pondus."""
    sys.path.insert(1, os.path.join(srcdir, 'src'))
    from pondus import __version__
    return __version__

def create_pot(version, potfiles):
    """Creates pondus.pot, the template file for translations."""
    command = 'xgettext'
    command += ' -L Python'
    command += ' -o pondus.pot'
    command += ' --package-name=Pondus'
    command += ' --package-version=' + version
    command += ' --msgid-bugs-address=eike@ephys.de '
    command += ' '.join(potfiles)
    os.system(command)
    return None

def update_po(languages):
    """Merges the existing .po files with the new pondus.pot."""
    for lang in languages:
        command = 'msgmerge --update ' + lang + '.po pondus.pot'
        os.system(command)
    return None


# list of source files containing translatable strings
potfiles = [os.path.join(srcdir, 'src/pondus/core/plot.py'),
            os.path.join(srcdir, 'src/pondus/core/util.py'),
            os.path.join(srcdir, 'src/pondus/gui/dialog_add.py'),
            os.path.join(srcdir, 'src/pondus/gui/dialog_plot.py'),
            os.path.join(srcdir, 'src/pondus/gui/dialog_remove.py'),
            os.path.join(srcdir, 'src/pondus/gui/dialog_wrong_format.py'),
            os.path.join(srcdir, 'src/pondus/gui/window_main.py')]
# list of existing translations
languages = ['de']
version = get_version()

create_pot(version, potfiles)
update_po(languages)
