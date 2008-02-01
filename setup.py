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

tmpscriptdir = 'src/scripts/'
mandir = 'share/man/man1'
desktopdir = 'share/applications'
docdir = 'share/doc/pondus'
buttondir = 'share/pondus'
pixmapdir = 'share/pixmaps'
icondir_48 = 'share/icons/hicolor/48x48/apps'
icondir_scalable = 'share/icons/hicolor/scalable/apps'

def get_version():
    """Returns the current version of Pondus."""
    sys.path.insert(1, os.getcwd()+'/src')
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
            scriptpath = tmpscriptdir + 'pondus-win.py'
        else:
            scriptpath = tmpscriptdir + 'pondus'
        if not os.path.exists(tmpscriptdir):
            os.makedirs(tmpscriptdir)
        shutil.copyfile('src/pondus.py', scriptpath)
        return [scriptpath]

def clean_up():
    """Removes the temporarily generated data."""
    if os.path.exists(tmpscriptdir):
        shutil.rmtree(tmpscriptdir)

setup(name = 'pondus',
      version = get_version(),
      description = 'Pondus is a personal weight manager.',
      author = 'Eike Nicklas',
      author_email = 'eike@ephys.de',
      url = 'http://www.ephys.de/software/pondus/',
      license = 'GPL',
      scripts = get_scripts(),
      data_files = [(desktopdir, ['data/pondus.desktop']),
                    (mandir, ['data/pondus.1.gz']),
                    (docdir, ['NEWS', 'README', 'TODO']),
                    (buttondir, ['data/icons/plot.png']),
                    (pixmapdir, ['data/icons/pondus.xpm']),
                    (icondir_48, ['data/icons/pondus.png']),
                    (icondir_scalable, ['data/icons/pondus.svg'])],
      package_dir = {'pondus': 'src/pondus'},
      packages = ['pondus', 'pondus.core', 'pondus.gui'],
      requires = ['python(>= 2.4)', 'pygtk(>=2.4)', 'matplotlib']
)

clean_up()
