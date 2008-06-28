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

from pondus import parameters


class PreferencesDialog(object):
    """Displays the preferences dialog."""

    def __init__(self):
        self.newconfig = dict(parameters.config)

        self.dialog = gtk.Dialog(flags=gtk.DIALOG_NO_SEPARATOR)
        self.dialog.set_title(_('Preferences'))

        unit_box = gtk.VBox()
        unit_box.set_border_width(5)
        unit_label = gtk.Label(_('Weight Unit:'))
        unit_label.set_alignment(xalign=0, yalign=0.5)
        unit_box.pack_start(unit_label)
        self.unit_button = gtk.RadioButton(label='kg')
        if self.newconfig['preferences.weight_unit'] == 'kg':
            self.unit_button.set_active(True)
        self.unit_button.connect('toggled', self.on_unit_change, 'kg')
        unit_box.pack_start(self.unit_button)
        self.unit_button = gtk.RadioButton(group=self.unit_button, label='lbs')
        if self.newconfig['preferences.weight_unit'] == 'lbs':
            self.unit_button.set_active(True)
        self.unit_button.connect('toggled', self.on_unit_change, 'lbs')
        unit_box.pack_start(self.unit_button)
        self.dialog.vbox.pack_start(unit_box)

        self.use_plan_button = gtk.CheckButton(_('Use Weight Planner'))
        self.use_plan_button.set_border_width(5)
        self.use_plan_button.set_active( \
                        self.newconfig['preferences.use_weight_plan'])
        self.dialog.vbox.pack_start(self.use_plan_button)

        self.remember_button = gtk.CheckButton(_('Remember Window Size'))
        self.remember_button.set_border_width(5)
        self.remember_button.set_active(self.newconfig['window.remember_size'])
        self.dialog.vbox.pack_start(self.remember_button)

        # buttons in action area
        self.dialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        self.dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)

        self.dialog.show_all()

    def run(self):
        """Runs the dialog and updates the configuration."""
        response = self.dialog.run()
        if response == gtk.RESPONSE_OK:
            self.newconfig['window.remember_size'] = \
                                    self.remember_button.get_active()
            self.newconfig['preferences.use_weight_plan'] = \
                                    self.use_plan_button.get_active()
            parameters.config = self.newconfig
        self.dialog.hide()
        return None

    # callback functions
    def on_unit_change(self, widget, data):
        """Remembers the selected weight unit to be saved later."""
        if widget.get_active():
            self.newconfig['preferences.weight_unit'] = data
        return None
