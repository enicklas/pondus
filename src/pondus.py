#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Pondus is a personal weight manager.
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

from pondus.core import option_parser

if __name__ == '__main__':
    option_parser.parse_options()
    from pondus.core import initialize
    initialize.initialize()
    from pondus.gui.window_main import MainWindow
    pondus = MainWindow()
    pondus.main()
