# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2008-10  Eike Nicklas <eike@ephys.de>

This program is free software licensed under the MIT license. For details
see LICENSE or http://www.opensource.org/licenses/mit-license.php
"""

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
import os


class SaveFileDialog(object):
    """Allows the user to select a file something should be saved to."""

    def __init__(self, default_file_name, file_formats):
        self.chooser = Gtk.FileChooserDialog()
        self.chooser.set_action(Gtk.FileChooserAction.SAVE)
        self.chooser.set_title(_('Save to File'))

        self.chooser.set_current_folder(os.path.expanduser('~'))
        self.chooser.set_current_name(default_file_name)

        file_type_box = Gtk.HBox(homogeneous=False, spacing=10)
        file_type_label = Gtk.Label(label=_('Save as File Type:'))
        file_type_box.pack_start(file_type_label, False, False)
        self.filetypeselector = Gtk.ComboBoxText()
        for ending in file_formats:
            self.filetypeselector.append_text(ending)
        self.filetypeselector.set_active(0)
        file_type_box.pack_end(self.filetypeselector, True, True)
        self.chooser.vbox.pack_start(file_type_box, False, False)

        # connect the signals
        self.filetypeselector.connect('changed', self.update_file_ending)
        # buttons in action area
        self.chooser.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.chooser.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        # show the dialog
        self.chooser.show_all()

    def run(self, plot=None):
        """Runs the dialog and closes it afterwards."""
        response = self.chooser.run()
        if response == Gtk.ResponseType.OK:
            self.update_file_ending(self.filetypeselector)
            filename = self.chooser.get_filename()
            if plot is not None:
                plot.save_to_file(filename)
            self.chooser.hide()
            return filename
        self.chooser.hide()

    def update_file_ending(self, filetypeselector):
        """Updates the file ending of the target file."""
        ending = filetypeselector.get_active_text()
        filename = os.path.split(self.chooser.get_filename())[1]
        filebase = os.path.splitext(filename)[0]
        self.chooser.set_current_name(filebase + ending)
