#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2008-09  Eike Nicklas <eike@ephys.de>

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


def get_version():
    """Returns the current version of Pondus."""
    srcdir = os.path.dirname(os.path.abspath(sys.path[0]))
    sys.path.insert(1, os.path.join(srcdir, 'src'))
    from pondus import __version__
    return __version__

def get_language_codes():
    """Returns a list of language codes of available translations"""
    language_codes = []
    podir = '.'
    for file_ in os.listdir(podir):
        if not file_.endswith('.po'):
            continue
        language_codes.append(os.path.splitext(file_)[0])
    return language_codes

def create_pot(version, potfiles):
    """Creates pondus.pot, the template file for translations."""
    command = 'xgettext'
    command += ' -L Python'
    command += ' -o pondus.pot'
    command += ' --package-name=Pondus'
    command += ' --package-version=' + version
    command += ' --msgid-bugs-address=pondus-dev@sharesource.org '
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
potfiles = [('../src/pondus/core/initialize.py'),
            ('../src/pondus/core/filelock.py'),
            ('../src/pondus/core/option_parser.py'),
            ('../src/pondus/core/plot.py'),
            ('../src/pondus/core/util.py'),
            ('../src/pondus/gui/dialog_add.py'),
            ('../src/pondus/gui/dialog_csv_export.py'),
            ('../src/pondus/gui/dialog_csv_import.py'),
            ('../src/pondus/gui/dialog_plot.py'),
            ('../src/pondus/gui/dialog_preferences.py'),
            ('../src/pondus/gui/dialog_save_file.py'),
            ('../src/pondus/gui/dialog_select_file.py'),
            ('../src/pondus/gui/window_main.py')]

languages = get_language_codes()
version = get_version()

create_pot(version, potfiles)
update_po(languages)
