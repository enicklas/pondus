#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2008-09  Eike Nicklas <eike@ephys.de>

This program is free software licensed under the MIT license. For details
see LICENSE or http://www.opensource.org/licenses/mit-license.php
"""

import os, sys


def _get_version():
    """Returns the current version of Pondus."""
    srcdir = os.path.dirname(os.path.abspath(sys.path[0]))
    sys.path.insert(1, srcdir)
    from pondus import __version__
    return __version__

def _get_language_codes():
    """Returns a list of language codes of available translations"""
    language_codes = []
    podir = '.'
    for file_ in os.listdir(podir):
        if not file_.endswith('.po'):
            continue
        language_codes.append(os.path.splitext(file_)[0])
    return language_codes

def _create_pot(version, files_to_translate):
    """Creates pondus.pot, the template file for translations."""
    gettext_command = ['xgettext']
    gettext_options = [
            '-L Python',
            '-o pondus.pot',
            '--package-name=Pondus',
            ''.join(['--package-version=', version]),
            '--msgid-bugs-address=pondus-dev@sharesource.org']
    gettext_command.extend(gettext_options)
    gettext_command.extend(files_to_translate)
    os.system(' '.join(gettext_command))
    return None

def _update_po(languages):
    """Merges the existing .po files with the new pondus.pot."""
    for lang in languages:
        command = 'msgmerge --update ' + lang + '.po pondus.pot'
        os.system(command)
    return None

if __name__ == '__main__':
    # list of source files containing translatable strings
    files_to_translate = []
    for root, dirs, files in os.walk('../pondus/'):
        for f in files:
            if os.path.splitext(f)[1] == '.py':
                files_to_translate.append(os.path.join(root, f))
    # list of existing translations
    languages = _get_language_codes()
    version = _get_version()

    _create_pot(version, files_to_translate)
    _update_po(languages)
