# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2007-11  Eike Nicklas <eike@ephys.de>

This program is free software licensed under the MIT license. For details
see LICENSE or http://www.opensource.org/licenses/mit-license.php
"""

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from gi.repository import GObject
from datetime import date, timedelta

from pondus.core import parameters
from pondus.core import util
from pondus.gui.dialog_message import MessageDialog


class AddDataDialog(object):
    """Implements the user interface to add or edit datasets."""

    def __init__(self, parent_window, dataset, edit):
        self.dataset = dataset
        # get default values for entry boxes
        if parameters.config['preferences.unit_system'] == 'imperial':
            weight = self.dataset.weight_lbs
        else:
            weight = self.dataset.weight
        if parameters.config['preferences.use_note']:
            note = self.dataset.note
            if note is None:
                note = ''

        self.dialog = Gtk.Dialog(parent=parent_window)
        # set the title
        if edit:
            self.dialog.set_title(_('Edit Dataset'))
        else:
            self.dialog.set_title(_('Add Dataset'))

        # get content area
        content_area = self.dialog.get_content_area()

        # create the labels and entry boxes
        date_box = Gtk.VBox(spacing=5)
        date_box.set_border_width(5)
        if parameters.config['preferences.use_calendar']:
            date_ = self.dataset.date
            date_label = Gtk.Label(label=_('Date') + ':')
            date_label.set_alignment(xalign=0, yalign=0.5)
            self.calendar = Gtk.Calendar()
            if parameters.config['preferences.unit_system'] == 'metric':
                self.calendar.set_display_options(
                                            Gtk.CalendarDisplayOptions.SHOW_HEADING |
                                            Gtk.CalendarDisplayOptions.SHOW_DAY_NAMES)
            self.calendar.select_month(date_.month-1, date_.year)
            self.calendar.select_day(date_.day)
            date_box.pack_start(date_label, False, True, 0)
            date_box.pack_start(self.calendar, False, True, 0)
        else:
            date_ = str(self.dataset.date)
            date_label = Gtk.Label(label=_('Date (YYYY-MM-DD)') + ':')
            date_label.set_alignment(xalign=0, yalign=0.5)
            self.date_entry = Gtk.Entry()
            self.date_entry.set_text(date_)
            self.date_entry.set_activates_default(True)
            date_box.pack_start(date_label, True, False, 0)
            date_box.pack_start(self.date_entry, False, True, 0)
        content_area.pack_start(date_box, False, True, 0)

        weight_bodyfat_box = Gtk.HBox(spacing=5)
        weight_box = Gtk.VBox(spacing=5)
        weight_box.set_border_width(5)
        weight_label = Gtk.Label(label=
                (_('Weight') + ' (' + util.get_weight_unit() + '):'))
        weight_label.set_alignment(xalign=0, yalign=0.5)
        weight_adj = Gtk.Adjustment(value=weight, lower=0, upper=1000,
                                    step_incr=0.1, page_incr=1.0)
        self.weight_entry = Gtk.SpinButton(adjustment=weight_adj, digits=1)
        self.weight_entry.set_numeric(True)
        self.weight_entry.set_activates_default(True)
        weight_box.pack_start(weight_label, False, True, 0)
        weight_box.pack_start(self.weight_entry, False, True, 0)
        weight_bodyfat_box.pack_start(weight_box, True, True, 0)

        if parameters.config['preferences.use_bodyfat']:
            bodyfat_box = self._get_percentage_box('bodyfat')
            weight_bodyfat_box.pack_start(bodyfat_box, True, True, 0)

        content_area.pack_start(weight_bodyfat_box, False, True, 0)

        muscle_water_box = Gtk.HBox(spacing=5)
        if parameters.config['preferences.use_muscle']:
            muscle_box = self._get_percentage_box('muscle')
            muscle_water_box.pack_start(muscle_box, True, True, 0)
        if parameters.config['preferences.use_water']:
            water_box = self._get_percentage_box('water')
            muscle_water_box.pack_start(water_box, True, True, 0)
        content_area.pack_start(muscle_water_box, False, True, 0)

        if parameters.config['preferences.use_note']:
            note_box = Gtk.VBox(spacing=5)
            note_box.set_border_width(5)
            textwindow = Gtk.ScrolledWindow()
            textwindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
            note_label = Gtk.Label(label=_('Note') + ':')
            note_label.set_alignment(xalign=0, yalign=0.5)
            self.note_view = Gtk.TextView()
            self.note_view.set_editable(True)
            self.note_view.set_wrap_mode(Gtk.WrapMode.WORD)
            self.note_buffer = self.note_view.get_buffer()
            self.note_buffer.set_text(note)
            textwindow.add(self.note_view)
            note_box.pack_start(note_label, False, True, 0)
            note_box.pack_start(textwindow, True, True, 0)
            content_area.pack_start(note_box, True, True, 0)

        # buttons in action area
        self.dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.dialog.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)

        self.dialog.set_default_response(Gtk.ResponseType.OK)

        # connect the signals
        self.weight_insert_signal = \
                self.weight_entry.connect('insert_text', self.on_insert)
        if parameters.config['preferences.use_bodyfat']:
            self.bodyfat_insert_signal = \
                self.bodyfat_entry.connect('insert_text', self.on_insert)
        if parameters.config['preferences.use_muscle']:
            self.muscle_insert_signal = \
                self.muscle_entry.connect('insert_text', self.on_insert)
        if parameters.config['preferences.use_water']:
            self.water_insert_signal = \
                self.water_entry.connect('insert_text', self.on_insert)
        if not parameters.config['preferences.use_calendar']:
            self.date_entry.connect('focus-in-event', self.on_focus)
            self.date_insert_signal = \
                    self.date_entry.connect('insert_text', self.on_insert)

        # show the content
        self.dialog.show_all()

    def run(self):
        """Runs the dialog and returns the new/updated dataset."""
        response = self.dialog.run()
        if response == Gtk.ResponseType.OK:
            # try to create a new dataset from the given data
            try:
                if parameters.config['preferences.use_calendar']:
                    updated_year, updated_month, updated_day = \
                            self.calendar.get_date()
                    self.dataset.date = \
                            date(updated_year, updated_month+1, updated_day)
                else:
                    self.dataset.date = \
                            util.str2date(self.date_entry.get_text())
                if parameters.config['preferences.unit_system'] == 'imperial':
                    self.dataset.weight_lbs = self.weight_entry.get_value()
                else:
                    self.dataset.weight = self.weight_entry.get_value()
                for key in ['bodyfat', 'muscle', 'water']:
                    if parameters.config['preferences.use_' + key]:
                        data = getattr(self, key+'_entry').get_value()
                        if data > 0.1:
                            setattr(self.dataset, key, data)
                        else:
                            setattr(self.dataset, key, None)
                if parameters.config['preferences.use_note']:
                    note = self.note_buffer.get_text(
                            self.note_buffer.get_start_iter(),
                            self.note_buffer.get_end_iter(),
                            False).strip()
                    if note != '':
                        self.dataset.note = note
                    else:
                        self.dataset.note = None
            except:
                title = _('Error: Wrong Format')
                message = _('The data entered is not in the correct format!')
                MessageDialog(
                        type_='error', title=title, message=message).run()
                return self.run()
            self.dialog.hide()
            return self.dataset
        else:
            self.dialog.hide()
            return None

    # callback methods
    def on_focus(self, entry, event):
        """Prevents a selection and puts the cursor at the end
        of the entry instead."""
        GObject.idle_add(entry.set_position, -1)

    def on_insert(self, entry, text, length, position):
        """Prevents '+' and '-' from being inserted into the entry and
        triggers the appropriate callback function instead."""
        if text in ['+', '-']:
            position = entry.get_position()
            entry.emit_stop_by_name('insert_text')
            # check first for use_calendar; date_entry might not exist
            if (not parameters.config['preferences.use_calendar']
                            and entry == self.date_entry):
                GObject.idle_add(self.date_key_press, entry, text, position)
            if entry == self.weight_entry \
                    or (parameters.config['preferences.use_bodyfat'] \
                        and entry==self.bodyfat_entry) \
                    or (parameters.config['preferences.use_muscle'] \
                        and entry==self.muscle_entry) \
                    or (parameters.config['preferences.use_water'] \
                        and entry==self.water_entry):
                GObject.idle_add(self.spin_key_press, entry, text)

    # helper methods
    def date_key_press(self, entry, text, position):
        """Tests, which key was pressed and increments/decrements the
        date in date entry by one day if possible."""
        try:
            date_ = util.str2date(entry.get_text())
        except ValueError:
            entry.handler_block(self.date_insert_signal)
            orig_text = entry.get_text()
            new_text = orig_text[:position] + text + orig_text[position:]
            entry.set_text(new_text)
            entry.set_position(position+1)
            entry.handler_unblock(self.date_insert_signal)
            return
        else:
            if text == '+':
                date_ += timedelta(days=1)
            elif text == '-':
                date_ -= timedelta(days=1)
            entry.handler_block(self.date_insert_signal)
            entry.set_text(str(date_))
            entry.set_position(-1)
            entry.handler_unblock(self.date_insert_signal)

    def spin_key_press(self, entry, text):
        """Tests, which key was pressed and increments/decrements the
        value in the given entry by 0.1 if possible."""
        if text == '+':
            entry.spin(Gtk.SpinType.STEP_FORWARD, increment=0.1)
        elif text == '-':
            entry.spin(Gtk.SpinType.STEP_BACKWARD, increment=0.1)

    def _get_percentage_box(self, key):
        """Returns a box containing label and spinbutton for entering one of
        bodyfat, muscle or water percentage."""
        if parameters.config['preferences.use_' + key]:
            box = Gtk.VBox(spacing=5)
            box.set_border_width(5)
            if key == 'bodyfat':
                label = Gtk.Label(label=_('Bodyfat') + ' (%):')
            if key == 'muscle':
                label = Gtk.Label(label=_('Muscle') + ' (%):')
            if key == 'water':
                label = Gtk.Label(label=_('Water') + ' (%):')
            label.set_alignment(xalign=0, yalign=0.5)
            data = getattr(self.dataset, key)
            if data is None:
                data = 0.0
            adj = Gtk.Adjustment(value=data, lower=0, upper=100,
                                        step_incr=0.1, page_incr=1.0)
            entry = Gtk.SpinButton(adjustment=adj, digits=1)
            entry.set_numeric(True)
            entry.set_activates_default(True)
            setattr(self, key+'_entry', entry)
            box.pack_start(label, False, True, 0)
            box.pack_start(entry, False, True, 0)
            return box
