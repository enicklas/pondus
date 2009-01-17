#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2007-09  Eike Nicklas <eike@ephys.de>

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
import gobject
from datetime import date, timedelta

from pondus import parameters
from pondus.core import util
from pondus.gui.dialog_message import MessageDialog


class AddDataDialog(object):
    """Implements the user interface to add or edit datasets."""

    def __init__(self, dataset, edit):
        self.dataset = dataset
        # get default values for entry boxes
        ddate = self.dataset.get('date')
        weight = self.dataset.get('weight')
        if parameters.config['preferences.unit_system'] == 'imperial':
            weight = util.kg_to_lbs(weight)
        weight = round(weight, 1)

        self.dialog = gtk.Dialog(flags=gtk.DIALOG_NO_SEPARATOR)
        # set the title
        if edit == False:
            self.dialog.set_title(_('Add Dataset'))
        else:
            self.dialog.set_title(_('Edit Dataset'))

        # create the labels and entry boxes
        date_box = gtk.VBox(spacing=5)
        date_box.set_border_width(5)
        date_label = gtk.Label(_('Date:'))
        date_label.set_alignment(xalign=0, yalign=0.5)
        self.calendar = gtk.Calendar()
        if parameters.config['preferences.unit_system'] == 'metric':
            self.calendar.set_display_options( \
                                        gtk.CALENDAR_SHOW_HEADING | \
                                        gtk.CALENDAR_SHOW_DAY_NAMES | \
                                        gtk.CALENDAR_WEEK_START_MONDAY)
        self.calendar.select_month(ddate.month-1, ddate.year)
        self.calendar.select_day(ddate.day)
        
        date_box.pack_start(date_label)
        date_box.pack_start(self.calendar)

        weight_box = gtk.VBox(spacing=5)
        weight_box.set_border_width(5)
        weight_label = gtk.Label(_('Weight') + ' (' \
            + util.get_weight_unit() + '):')
        weight_label.set_alignment(xalign=0, yalign=0.5)
        weight_adj = gtk.Adjustment(
                                value=weight,
                                lower=0,
                                upper=1000,
                                step_incr=0.1,
                                page_incr=1.0)
        self.weight_entry = gtk.SpinButton(adjustment=weight_adj, digits=1)
        self.weight_entry.set_numeric(True)
        self.weight_entry.set_activates_default(True)
        weight_box.pack_start(weight_label)
        weight_box.pack_start(self.weight_entry)

        self.dialog.vbox.pack_start(date_box)
        self.dialog.vbox.pack_start(weight_box)

        # buttons in action area
        self.dialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        self.dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)

        self.dialog.set_default_response(gtk.RESPONSE_OK)

        # connect the signals
        self.weight_insert_signal = \
                self.weight_entry.connect('insert_text', self.on_insert)

        # show the content
        self.dialog.show_all()
        return None

    def run(self):
        """Runs the dialog and returns the new/updated dataset."""
        response = self.dialog.run()
        if response == gtk.RESPONSE_OK:
            # try to create a new dataset from the given data
            updated_year, updated_month, updated_day = self.calendar.get_date()
            updated_date = date(updated_year, updated_month+1, updated_day)
            weightstring = self.weight_entry.get_text()
            try:
                updated_weight = self.weight_entry.get_value()
                if parameters.config['preferences.unit_system'] == 'imperial':
                    updated_weight = round(util.lbs_to_kg(updated_weight), 2)
            except:
                title = _('Error: Wrong Format')
                message = _('The data entered is not in the correct format!')
                MessageDialog(type='error', title=title, message=message).run()
                return self.run()
            self.dataset.set('date', updated_date)
            self.dataset.set('weight', updated_weight)
            self.dialog.hide()
            return self.dataset
        else:
            self.dialog.hide()
            return None


    # callback functions

    def on_focus(self, entry, event):
        """Prevents a selection and puts the cursor at the end
        of the entry instead."""
        gobject.idle_add(entry.set_position, -1)
        return None

    def on_insert(self, entry, text, length, *args):
        """Prevents '+' and '-' from being inserted into the entry and
        triggers the appropriate callback function in stead."""
        if text in ['+', '-']:
            position = entry.get_position()
            entry.emit_stop_by_name('insert_text')
            gobject.idle_add(self.weight_key_press, text)
        return None

    def weight_key_press(self, text):
        """Tests, which key was pressed and increments/decrements the
        value in the weight entry by 0.1 if possible."""
        if text == '+':
            self.weight_entry.spin(gtk.SPIN_STEP_FORWARD, increment=0.1)
        elif text == '-':
            self.weight_entry.spin(gtk.SPIN_STEP_BACKWARD, increment=0.1)
        return None
