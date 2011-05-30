#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2007-11  Eike Nicklas <eike@ephys.de>

This program is free software licensed under the MIT license. For details
see LICENSE or http://www.opensource.org/licenses/mit-license.php
"""

from distutils.core import setup
import os
import shutil
import sys

from pondus import __version__


tmpdir = 'tmp'
podir = 'po'
modir = 'po/mo'


def _get_language_codes():
    """Returns a list of language codes of available translations"""
    language_codes = []
    for file_ in os.listdir(podir):
        if not file_.endswith('.po'):
            continue
        language_codes.append(os.path.splitext(file_)[0])
    return language_codes


def _get_scripts():
    """Returns the main script without .py extension. On windows,
    a script with an extension is used. When building a source
    distribution, no script is returned."""
    if sys.argv[1] == 'sdist':
        return []
    else:
        if sys.platform == 'win32':
            scriptpath = os.path.join(tmpdir, 'pondus-win.py')
        else:
            scriptpath = os.path.join(tmpdir, 'pondus')
        if not os.path.exists(tmpdir):
            os.makedirs(tmpdir)
        shutil.copyfile('pondus.py', scriptpath)
        return [scriptpath]


def _create_mo():
    """Creates the .mo files to be distributed with the source."""
    if not os.path.exists(modir):
        for lang in _get_language_codes():
            pofile = os.path.join('po', lang + '.po')
            modir_lang = os.path.join(modir, lang, 'LC_MESSAGES')
            mofile = os.path.join(modir_lang, 'pondus.mo')
            if not os.path.exists(modir_lang):
                os.makedirs(modir_lang)
            print 'generating', mofile
            os.system('msgfmt %s -o %s' % (pofile, mofile))


def _create_man():
    """Creates the gzipped man file to be distributed with the source."""
    if not os.path.exists('data/pondus.1.gz'):
        os.system('a2x -f manpage data/pondus.1.txt')
        os.system('gzip -9 data/pondus.1')


def _clean_up():
    """Removes the temporarily generated data."""
    if os.path.exists(tmpdir):
        shutil.rmtree(tmpdir)


long_description = """
Pondus is a personal weight manager that keeps track of your body
weight and, optionally, the percentage of bodyfat, muscle and water.
It aims to be simple to use, lightweight and fast. All data
can be plotted to get a quick overview of the history of your weight.
A simple weight planner allows to define "target weights" and this
plan can be compared with the actual measurements in a plot.
"""

data_files = [
        ('share/applications', ['data/pondus.desktop']),
        ('share/man/man1', ['data/pondus.1.gz']),
        ('share/doc/pondus', ['AUTHORS', 'NEWS', 'README', 'TODO']),
        ('share/pondus', ['data/icons/plot.png']),
        ('share/pixmaps', ['data/icons/pondus.xpm']),
        ('share/icons/hicolor/48x48/apps', ['data/icons/pondus.png']),
        ('share/icons/hicolor/scalable/apps', ['data/icons/pondus.svg'])]
for lang in _get_language_codes():
    data_files.append((os.path.join('share/locale', lang, 'LC_MESSAGES'),
            [os.path.join(modir, lang, 'LC_MESSAGES/pondus.mo')]))

_create_mo()
_create_man()

setup(name = 'pondus',
      version = __version__,
      description = 'personal weight manager',
      long_description = long_description,
      author = 'Eike Nicklas',
      author_email = 'eike@ephys.de',
      url = 'http://bitbucket.org/eike/pondus/',
      license = 'MIT',
      scripts = _get_scripts(),
      data_files = data_files,
      package_dir = {'pondus': 'pondus'},
      packages = ['pondus', 'pondus.backends', 'pondus.core', 'pondus.gui'],
      requires = ['python(>= 2.5)', 'pygtk(>=2.12)', 'matplotlib'])

_clean_up()
