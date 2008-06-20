#! /usr/bin/env python
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

from pondus import parameters, user_data
from pondus.core import csv_parser
from pondus.gui.dialog_message import MessageDialog
from pondus.gui.dialog_save_file import SaveFileDialog


class CSVDialogExport(object):
    """Displays the csv export dialog."""

    def __init__(self):
        self.dialog = gtk.Dialog(flags=gtk.DIALOG_NO_SEPARATOR)
        self.dialog.set_title(_('CSV Export'))

        self.datasetdata = user_data.user.measurements
        self.filename = _('weight.csv')

        databox = gtk.VBox()
        databox.set_border_width(5)
        data_label = gtk.Label(_('Data to export:'))
        data_label.set_alignment(xalign=0, yalign=0.5)
        databox.pack_start(data_label)
        self.data_button = gtk.RadioButton(label=_('Weight Measurements'))
        self.data_button.set_active(True)
        self.data_button.connect('toggled', self.on_data_change, 'meas')
        databox.pack_start(self.data_button)
        self.data_button = gtk.RadioButton(group=self.data_button, \
                                           label=_('Weight Plan'))
        self.data_button.connect('toggled', self.on_data_change, 'plan')
        if not parameters.config['preferences.use_weight_plan']:
            self.data_button.set_sensitive(False)
        databox.pack_start(self.data_button)
        self.dialog.vbox.pack_start(databox)

        filebox = gtk.VBox()
        filebox.set_border_width(5)
        file_label = gtk.Label(_('CSV File to save to:'))
        file_label.set_alignment(xalign=0, yalign=0.5)
        filebox.pack_start(file_label)
        filehbox = gtk.HBox(homogeneous=False, spacing=5)
        self.file_entry = gtk.Entry()
        self.file_entry.set_text(os.path.join(os.path.expanduser('~'), \
                                 self.filename))
        filehbox.pack_start(self.file_entry)
        choose_button = gtk.Button(stock=gtk.STOCK_OPEN)
        filehbox.pack_start(choose_button)
        filebox.pack_start(filehbox)
        self.dialog.vbox.pack_start(filebox)

        # buttons in action area
        self.dialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        self.dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)

        # connect the signals
        choose_button.connect('clicked', self.select_file)

        # show the content
        self.dialog.show_all()

    def run(self):
        """Runs the dialog and closes it afterwards."""
        response = self.dialog.run()
        if response == gtk.RESPONSE_OK:
            self.exportcsv()
        self.dialog.hide()

    def exportcsv(self):
        """Saves the datasetdata to a csv file."""
        csvpath = os.path.expanduser(self.file_entry.get_text())
        csv_parser.write_csv(self.datasetdata, csvpath)
        title = _('Export successful')
        message = _('The export was successful.')
        MessageDialog(type='info', title=title, message=message).run()

    def select_file(self, button):
        """Runs the file selection dialog and updates the file entry
        accordingly."""
        newpath = SaveFileDialog(self.filename, ['.csv']).run(None)
        if newpath is not None:
            self.file_entry.set_text(newpath)

    def on_data_change(self, widget, key):
        """Updates the datasetdata to be exported."""
        if widget.get_active():
            if key == 'meas':
                self.datasetdata = user_data.user.measurements
            elif key == 'plan':
                self.datasetdata = user_data.user.plan
