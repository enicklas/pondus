#! /usr/bin/env python
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

from distutils.core import setup
import os, shutil, sys


tmpdir = 'tmp'
podir = 'po'
modir = 'po/mo'

def get_version():
    """Returns the current version of Pondus."""
    srcdir = os.path.abspath(sys.path[0])
    sys.path.insert(1, os.path.join(srcdir, 'src'))
    from pondus import __version__
    return __version__

def get_language_codes():
    """Returns a list of language codes of available translations"""
    language_codes = []
    for file_ in os.listdir(podir):
        if not file_.endswith('.po'):
            continue
        language_codes.append(os.path.splitext(file_)[0])
    return language_codes

def get_scripts():
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
        shutil.copyfile('src/pondus.py', scriptpath)
        return [scriptpath]

def create_mo():
    """Creates the .mo files to be distributed with the source."""
    if not os.path.exists(modir):
        for lang in get_language_codes():
            pofile = os.path.join('po', lang + '.po')
            modir_lang = os.path.join(modir, lang, 'LC_MESSAGES')
            mofile = os.path.join(modir_lang, 'pondus.mo')
            if not os.path.exists(modir_lang):
                os.makedirs(modir_lang)
            print 'generating', mofile
            os.system('msgfmt %s -o %s' % (pofile, mofile))

def create_man():
    """Creates the gzipped man file to be distributed with the source."""
    if not os.path.exists('data/pondus.1.gz'):
        os.system('a2x -f manpage data/pondus.1.txt')
        os.system('gzip -9 data/pondus.1')

def build_manifest_in():
    files_to_include = ['AUTHORS', 'CONTRIBUTING', 'COPYING', 'INSTALL', \
            'NEWS', 'README', 'TODO', 'data/pondus.desktop', \
            'data/pondus.1.gz', 'data/icons/plot.png', \
            'data/icons/pondus.png', 'data/icons/pondus.svg', \
            'data/icons/pondus.xpm', 'src/pondus.py', \
            'po/README', 'po/update_po.py', 'po/pondus.pot']
    for lang in get_language_codes():
        files_to_include.append(os.path.join(podir, '.'.join([lang, 'po'])))
        files_to_include.append(os.path.join(modir, lang, \
                                                'LC_MESSAGES', 'pondus.mo'))
    manifest_in = open('MANIFEST.in', 'w')
    for file in files_to_include:
        manifest_in.write('include ' + file + '\n')
    manifest_in.close()

def clean_up():
    """Removes the temporarily generated data."""
    if os.path.exists(tmpdir):
        shutil.rmtree(tmpdir)

long_description = """
Pondus keeps track of your body weight. It aims to be simple to use,
lightweight and fast. The data can be plotted to get a quick overview
of the history of your weight. A simple weight planner allows to
define "target weights" and this plan can be compared with the actual
measurements in a plot.
"""

data_files = [
        ('share/applications', ['data/pondus.desktop']),
        ('share/man/man1', ['data/pondus.1.gz']),
        ('share/doc/pondus', ['AUTHORS', 'NEWS', 'README', 'TODO']),
        ('share/pondus', ['data/icons/plot.png']),
        ('share/pixmaps', ['data/icons/pondus.xpm']),
        ('share/icons/hicolor/48x48/apps', ['data/icons/pondus.png']),
        ('share/icons/hicolor/scalable/apps', ['data/icons/pondus.svg'])]
for lang in get_language_codes():
    data_files.append((os.path.join('share/locale', lang, 'LC_MESSAGES'), \
            [os.path.join(modir, lang, 'LC_MESSAGES/pondus.mo')]))

build_manifest_in()
create_mo()
create_man()

setup(name = 'pondus',
      version = get_version(),
      description = 'personal weight manager',
      long_description = long_description,
      author = 'Eike Nicklas',
      author_email = 'eike@ephys.de',
      url = 'http://www.ephys.de/software/pondus/',
      license = 'GPLv3+',
      scripts = get_scripts(),
      data_files = data_files,
      package_dir = {'pondus': 'src/pondus'},
      packages = ['pondus', 'pondus.core', 'pondus.gui'],
      requires = ['python(>= 2.4)', 'pygtk(>=2.6)', 'matplotlib']
      )

clean_up()
