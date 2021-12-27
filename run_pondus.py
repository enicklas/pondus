#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Pondus is a personal weight manager.
Copyright (C) 2007-21  Eike Nicklas <eike@ephys.de>

This program is free software licensed under the MIT license. For details
see LICENSE or http://www.opensource.org/licenses/mit-license.php
"""

def run():
    from pondus.core import initialize
    initialize.initialize()
    from pondus.gui.window_main import mainwindow
    mainwindow.main()

if __name__ == '__main__':
    run()
