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

__all__ = ['core', 'gui', 'datasets', 'parameters']
__version__ = '0.4.0'

import gettext
import os
import sys

def gettext_install():
    """Installs string translations; uses local data if available."""
    basepath = os.path.dirname(os.path.abspath(sys.path[0]))
    if os.path.exists(os.path.join(basepath, 'po/mo')):
        gettext.install('pondus', os.path.join(basepath, 'po/mo'))
    else:
        gettext.install('pondus', os.path.join(basepath, 'share/locale'))

gettext_install()
