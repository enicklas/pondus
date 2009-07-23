# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2008-09  Eike Nicklas <eike@ephys.de>

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


class SaveFileDialog(object):
    """Allows the user to select a file something should be saved to."""

    def __init__(self, default_file_name, file_formats):
        self.chooser = gtk.FileChooserDialog()
        self.chooser.set_action(gtk.FILE_CHOOSER_ACTION_SAVE)
        self.chooser.set_title(_('Save to File'))

        self.chooser.set_current_folder(os.path.expanduser('~'))
        self.chooser.set_current_name(default_file_name)

        file_type_box = gtk.HBox(homogeneous=False, spacing=10)
        file_type_label = gtk.Label(_('Save as File Type:'))
        file_type_box.pack_start(file_type_label, False, False)
        self.filetypeselector = gtk.combo_box_new_text()
        for ending in file_formats:
            self.filetypeselector.append_text(ending)
        self.filetypeselector.set_active(0)
        file_type_box.pack_end(self.filetypeselector, True, True)
        self.chooser.vbox.pack_start(file_type_box, False, False)

        # connect the signals
        self.filetypeselector.connect('changed', self.update_file_ending)

        # buttons in action area
        self.chooser.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        self.chooser.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)

        self.chooser.show_all()


    def run(self, plot):
        """Runs the dialog and closes it afterwards."""
        response = self.chooser.run()
        if response == gtk.RESPONSE_OK:
            self.update_file_ending(self.filetypeselector)
            if plot != None:
                plot.save_to_file(self.chooser.get_filename())
            self.chooser.hide()
            return self.chooser.get_filename()
        self.chooser.hide()

    def update_file_ending(self, filetypeselector):
        """Updates the file ending of the target file."""
        ending = filetypeselector.get_active_text()
        filename = os.path.split(self.chooser.get_filename())[1]
        filebase  = os.path.splitext(filename)[0]
        self.chooser.set_current_name(filebase + ending)
