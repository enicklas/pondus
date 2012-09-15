# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2008-11  Eike Nicklas <eike@ephys.de>

This program is free software licensed under the MIT license. For details
see LICENSE or http://www.opensource.org/licenses/mit-license.php
"""

import pygtk
pygtk.require('2.0')

import gtk
import os

from pondus.core import parameters
from pondus.backends.util import get_backend, imexport_backends
from pondus.gui.dialog_message import MessageDialog
from pondus.gui.dialog_save_file import SaveFileDialog
from pondus.gui.dialog_select_file import SelectFileDialog


class ImExportDialogBase(object):
    """Common base class for the ex-/import dialogs."""

    def __init__(self, title, data_label_text, file_label_text):
        self.dialog = gtk.Dialog(flags=gtk.DIALOG_NO_SEPARATOR)
        self.dialog.set_title(title)

        # get content area
        content_area = self.dialog.get_content_area()

        backendbox = gtk.VBox()
        backendbox.set_border_width(5)
        backend_label = gtk.Label(_('Select Backend:'))
        backend_label.set_alignment(xalign=0, yalign=0.5)
        backendbox.pack_start(backend_label, True, True, 0)
        backendselector = gtk.combo_box_new_text()
        for backend in imexport_backends:
            backendselector.append_text(backend)
        backendselector.set_active(0)
        backendbox.pack_start(backendselector, True, True, 0)
        content_area.pack_start(backendbox, True, True, 0)

        databox = gtk.VBox()
        databox.set_border_width(5)
        data_label = gtk.Label(data_label_text)
        data_label.set_alignment(xalign=0, yalign=0.5)
        databox.pack_start(data_label, True, True, 0)
        self.data_button = gtk.RadioButton(label=_('Weight Measurements'))
        self.data_button.set_active(True)
        self.data_button.connect('toggled', self.on_data_change, 'meas')
        self.on_data_change(self.data_button, 'meas')
        databox.pack_start(self.data_button, True, True, 0)
        self.data_button = gtk.RadioButton(
                            group=self.data_button, label=_('Weight Plan'))
        self.data_button.connect('toggled', self.on_data_change, 'plan')
        if not parameters.config['preferences.use_weight_plan']:
            self.data_button.set_sensitive(False)
        databox.pack_start(self.data_button, True, True, 0)
        content_area.pack_start(databox, True, True, 0)

        filebox = gtk.VBox()
        filebox.set_border_width(5)
        file_label = gtk.Label(file_label_text)
        file_label.set_alignment(xalign=0, yalign=0.5)
        filebox.pack_start(file_label, True, True, 0)
        filehbox = gtk.HBox(homogeneous=False, spacing=5)
        self.file_entry = gtk.Entry()
        filehbox.pack_start(self.file_entry, True, True, 0)
        choose_button = gtk.Button(stock=gtk.STOCK_OPEN)
        filehbox.pack_start(choose_button, True, True, 0)
        filebox.pack_start(filehbox, True, True, 0)
        content_area.pack_start(filebox, True, True, 0)

        # set initial backend
        self.update_backend(backendselector)

        # buttons in action area
        self.dialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        self.dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)

        # connect the signals
        choose_button.connect('clicked', self.select_file)
        backendselector.connect('changed', self.update_backend)

        # show the content
        self.dialog.show_all()

    def on_data_change(self, widget, key):
        """Updates the datasets to be im-/exported."""
        if widget.get_active():
            if key == 'meas':
                self.datasets = parameters.user.measurements
            elif key == 'plan':
                self.datasets = parameters.user.plan

    def update_backend(self, backendselector):
        """Updates backend and default filename."""
        backend = imexport_backends[backendselector.get_active()]
        self.backend = get_backend(backend)
        self.file_entry.set_text(self.backend.default_filename)


class DialogExport(ImExportDialogBase):
    """Constructs the export dialog."""

    def __init__(self):
        title = _('Export')
        data_label_text = _('Data to export:')
        file_label_text = _('File to save to:')
        ImExportDialogBase.__init__(self,
                title, data_label_text, file_label_text)

    def run(self):
        """Runs the dialog and closes it afterwards."""
        response = self.dialog.run()
        if response == gtk.RESPONSE_OK:
            self.export()
        self.dialog.hide()

    def export(self):
        """Saves the datasets to a file."""
        filepath = os.path.expanduser(self.file_entry.get_text())
        self.backend.write(self.datasets, filepath)
        title = _('Export successful')
        message = _('The export was successful.')
        MessageDialog(type_='info', title=title, message=message).run()

    def select_file(self, button):
        """Runs the file selection dialog and updates the file entry
        accordingly."""
        filepath = os.path.expanduser(self.file_entry.get_text())
        fileending = self.backend.fileending
        newpath = SaveFileDialog(filepath, ['.' + fileending]).run()
        if newpath is not None:
            self.file_entry.set_text(newpath)


class DialogImport(ImExportDialogBase):
    """Constructs the import dialog."""

    def __init__(self):
        title = _('Import')
        data_label_text = _('Import data to:')
        file_label_text = _('File to read from:')
        ImExportDialogBase.__init__(self,
                title, data_label_text, file_label_text)

    def run(self):
        """Runs the dialog and closes it afterwards."""
        response = self.dialog.run()
        if response == gtk.RESPONSE_OK:
            filepath = os.path.expanduser(self.file_entry.get_text())
            if os.path.isfile(filepath):
                self.import_(filepath)
            else:
                title = _('Error: Not a valid File')
                message = _('The given path does not point to a valid file!')
                MessageDialog(
                        type_='error', title=title, message=message).run()
                return self.run()
        self.dialog.hide()

    def import_(self, filepath):
        """Imports the data from the file."""
        new_datasets = self.backend.read(filepath)
        if new_datasets:
            self.datasets.add_list(new_datasets)
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
