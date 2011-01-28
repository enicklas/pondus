# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2008-11  Eike Nicklas <eike@ephys.de>

This program is free software licensed under the MIT license. For details
see LICENSE or http://www.opensource.org/licenses/mit-license.php
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
        # show the dialog
        self.chooser.show_all()

    def run(self):
        """Runs the dialog and closes it afterwards."""
        response = self.chooser.run()
        if response == gtk.RESPONSE_OK:
            filename = self.chooser.get_filename()
            self.chooser.hide()
            return filename
        self.chooser.hide()
