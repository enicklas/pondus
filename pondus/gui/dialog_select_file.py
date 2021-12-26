# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2008-11  Eike Nicklas <eike@ephys.de>

This program is free software licensed under the MIT license. For details
see LICENSE or http://www.opensource.org/licenses/mit-license.php
"""

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
import os


class SelectFileDialog(object):
    """Allows the user to select a file."""

    def __init__(self):
        self.chooser = Gtk.FileChooserDialog()
        self.chooser.set_action(Gtk.FileChooserAction.OPEN)
        self.chooser.set_title(_('Select File'))
        self.chooser.set_current_folder(os.path.expanduser('~'))
        # buttons in action area
        self.chooser.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.chooser.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        # show the dialog
        self.chooser.show_all()

    def run(self):
        """Runs the dialog and closes it afterwards."""
        response = self.chooser.run()
        if response == Gtk.ResponseType.OK:
            filename = self.chooser.get_filename()
            self.chooser.hide()
            return filename
        self.chooser.hide()
