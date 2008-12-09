# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2008  Eike Nicklas <eike@ephys.de>

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
import os

class SelectFileDialog(object):
    """Allows the user to select a file."""

    def __init__(self):
        self.chooser = gtk.FileChooserDialog()
        self.chooser.set_action(gtk.FILE_CHOOSER_ACTION_OPEN)
        self.chooser.set_title(_('Select File'))
        self.chooser.set_current_folder(os.path.expanduser('~'))

        # buttons in action area
        self.chooser.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        self.chooser.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)

        self.chooser.show_all()

    def run(self):
        """Runs the dialog and closes it afterwards."""
        response = self.chooser.run()
        if response == gtk.RESPONSE_OK:
            self.chooser.hide()
            return self.chooser.get_filename()
        self.chooser.hide()
        return None
