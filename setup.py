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

from distutils.core import setup
import os, shutil, sys


tmpdir = 'tmp'

def get_version():
    """Returns the current version of Pondus."""
    srcdir = os.path.abspath(sys.path[0])
    sys.path.insert(1, os.path.join(srcdir, 'src'))
    from pondus import __version__
    return __version__

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
    if sys.argv[1] == 'sdist':
        return None
    mo_dir = os.path.join(tmpdir, 'mo')
    for lang in ['de']:
        po_file = os.path.join('po', lang + '.po')
        mo_dir_lang = os.path.join(mo_dir, lang)
        mo_file = os.path.join(mo_dir_lang, 'pondus.mo')
        if not os.path.exists(mo_dir_lang):
            os.makedirs(mo_dir_lang)
        print 'generating', mo_file
        os.system('msgfmt %s -o %s' % (po_file, mo_file))

def clean_up():
    """Removes the temporarily generated data."""
    if os.path.exists(tmpdir):
        shutil.rmtree(tmpdir)

create_mo()

setup(name = 'pondus',
      version = get_version(),
      description = 'Pondus is a personal weight manager.',
      author = 'Eike Nicklas',
      author_email = 'eike@ephys.de',
      url = 'http://www.ephys.de/software/pondus/',
      license = 'GPL',
      scripts = get_scripts(),
      data_files = [
        ('share/applications', ['data/pondus.desktop']),
        ('share/man/man1', ['data/pondus.1.gz']),
        ('share/doc/pondus', ['AUTHORS', 'NEWS', 'README', 'TODO']),
        ('share/pondus', ['data/icons/plot.png']),
        ('share/pixmaps', ['data/icons/pondus.xpm']),
        ('share/icons/hicolor/48x48/apps', ['data/icons/pondus.png']),
        ('share/icons/hicolor/scalable/apps', ['data/icons/pondus.svg']),
        ('share/locale/de/LC_MESSAGES', [os.path.join(tmpdir, 'mo/de/pondus.mo')])],
      package_dir = {'pondus': 'src/pondus'},
      packages = ['pondus', 'pondus.core', 'pondus.gui'],
      requires = ['python(>= 2.4)', 'pygtk(>=2.4)', 'matplotlib']
)

clean_up()
