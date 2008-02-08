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

import gtk


class WrongFormatDialog(object):
    """Shows an error message, if the entered data can not be converted
    to a dataset object."""

    def __init__(self):
        self.dialog = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, \
        buttons=gtk.BUTTONS_CLOSE)

        self.dialog.set_title(_('Error: Wrong Format'))
        self.dialog.set_markup(_('The data entered is not in the correct format!'))

        self.dialog.show_all()

    def run(self):
        """Runs the dialog and closes it afterwards."""
        self.dialog.run()
        self.dialog.hide()
