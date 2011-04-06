# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2008-10  Eike Nicklas <eike@ephys.de>

This program is free software licensed under the MIT license. For details
see LICENSE or http://www.opensource.org/licenses/mit-license.php
"""

import pygtk
pygtk.require('2.0')

import gtk
import os

from pondus.core import parameters
from pondus.core import csv_parser
from pondus.gui.dialog_message import MessageDialog
from pondus.gui.dialog_save_file import SaveFileDialog
from pondus.gui.dialog_select_file import SelectFileDialog


class CSVDialogBase(object):
    """Common base class for the csv ex-/import dialogs."""

    def __init__(self, title, data_label_text, file_label_text):
        self.dialog = gtk.Dialog(flags=gtk.DIALOG_NO_SEPARATOR)
        self.dialog.set_title(title)

        self.datasets = parameters.user.measurements
        self.filename = _('weight.csv')

        databox = gtk.VBox()
        databox.set_border_width(5)
        data_label = gtk.Label(data_label_text)
        data_label.set_alignment(xalign=0, yalign=0.5)
        databox.pack_start(data_label)
        self.data_button = gtk.RadioButton(label=_('Weight Measurements'))
        self.data_button.set_active(True)
        self.data_button.connect('toggled', self.on_data_change, 'meas')
        databox.pack_start(self.data_button)
        self.data_button = gtk.RadioButton(
                            group=self.data_button, label=_('Weight Plan'))
        self.data_button.connect('toggled', self.on_data_change, 'plan')
        if not parameters.config['preferences.use_weight_plan']:
            self.data_button.set_sensitive(False)
        databox.pack_start(self.data_button)
        self.dialog.vbox.pack_start(databox)

        filebox = gtk.VBox()
        filebox.set_border_width(5)
        file_label = gtk.Label(file_label_text)
        file_label.set_alignment(xalign=0, yalign=0.5)
        filebox.pack_start(file_label)
        filehbox = gtk.HBox(homogeneous=False, spacing=5)
        self.file_entry = gtk.Entry()
        self.file_entry.set_text(
                    os.path.join(os.path.expanduser('~'), self.filename))
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

    def on_data_change(self, widget, key):
        """Updates the datasets to be im-/exported."""
        if widget.get_active():
            if key == 'meas':
                self.datasets = parameters.user.measurements
            elif key == 'plan':
                self.datasets = parameters.user.plan


class CSVDialogExport(CSVDialogBase):
    """Constructs the csv export dialog."""

    def __init__(self):
        title = _('CSV Export')
        data_label_text = _('Data to export:')
        file_label_text = _('CSV File to save to:')
        CSVDialogBase.__init__(self, title, data_label_text, file_label_text)

    def run(self):
        """Runs the dialog and closes it afterwards."""
        response = self.dialog.run()
        if response == gtk.RESPONSE_OK:
            self.exportcsv()
        self.dialog.hide()

    def exportcsv(self):
        """Saves the datasets to a csv file."""
        filepath = os.path.expanduser(self.file_entry.get_text())
        csv_parser.write_csv(self.datasets, filepath)
        title = _('Export successful')
        message = _('The export was successful.')
        MessageDialog(type_='info', title=title, message=message).run()

    def select_file(self, button):
        """Runs the file selection dialog and updates the file entry
        accordingly."""
        newpath = SaveFileDialog(self.filename, ['.csv']).run()
        if newpath is not None:
            self.file_entry.set_text(newpath)


class CSVDialogImport(CSVDialogBase):
    """Constructs the csv import dialog."""

    def __init__(self):
        title = _('CSV Import')
        data_label_text = _('Import data to:')
        file_label_text = _('CSV File to read from:')
        CSVDialogBase.__init__(self, title, data_label_text, file_label_text)

    def run(self):
        """Runs the dialog and closes it afterwards."""
        response = self.dialog.run()
        if response == gtk.RESPONSE_OK:
            filepath = os.path.expanduser(self.file_entry.get_text())
            if os.path.isfile(filepath):
                self.importcsv(filepath)
            else:
                title = _('Error: Not a valid File')
                message = _('The given path does not point to a valid file!')
                MessageDialog(
                        type_='error', title=title, message=message).run()
                return self.run()
        self.dialog.hide()

    def importcsv(self, filepath):
        """Imports the data from the csv file."""
        if csv_parser.read_csv(self.datasets, filepath):
            title = _('Import successful')
            message = _('The import was successful.')
            MessageDialog(type_='info', title=title, message=message).run()
        else:
            title = _('Import not successful')
            message = _('An error occured during the import.')
            MessageDialog(type_='error', title=title, message=message).run()

    def select_file(self, button):
        """Runs the file selection dialog and updates the file entry
        accordingly."""
        newpath = SelectFileDialog().run()
        if newpath is not None:
            self.file_entry.set_text(newpath)
