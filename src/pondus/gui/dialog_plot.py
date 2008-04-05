#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2007-08  Eike Nicklas <eike@ephys.de>

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
from datetime import date, timedelta

from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg \
    as FigureCanvas

from pondus import datasets, parameters
from pondus.core import util
from pondus.core.plot import Plot
from pondus.gui.dialog_message import MessageDialog
from pondus.gui.dialog_save_file import SaveFileDialog


class PlotDialog(object):
    """Implements the dialog to plot weight versus a selected time
    range."""

    def __init__(self):
        self.dialog = gtk.Dialog(title=_('Plot Weight'))
        self.dialog.set_default_size(600,400)

        # drawing area for the plot
        self.plot = Plot()
        self.canvas = FigureCanvas(self.plot.figure)
        self.dialog.vbox.set_spacing(5)
        self.dialog.vbox.pack_start(self.canvas)

        # date selection
        date_selection_box = gtk.HBox(homogeneous=False, spacing=5)

        date_label = gtk.Label(_('Select Date Range:'))
        date_selection_box.pack_start(date_label, False, False)

        self.start_date_entry = gtk.Entry()
        self.start_date_entry.set_width_chars(10)
        date_selection_box.pack_start(self.start_date_entry, False, False)

        date_selection_box.pack_start(gtk.Label('-'), False, False)

        self.end_date_entry = gtk.Entry()
        self.end_date_entry.set_width_chars(10)
        date_selection_box.pack_start(self.end_date_entry, False, False)

        self.dateselector = gtk.combo_box_new_text()
        self.dateselector.append_text(_('All Time'))
        self.dateselector.append_text(_('Last Year'))
        self.dateselector.append_text(_('Last Month'))
        self.dateselector.set_active(0)
        date_selection_box.pack_start(self.dateselector, True, False)

        date_update_button = gtk.Button(label=_('Update'))
        date_selection_box.pack_end(date_update_button, False, False)
        self.dialog.vbox.pack_start(date_selection_box, False, False)

        # buttons in action field
        save_button = gtk.Button(label=_('Save Plot'))
        self.dialog.action_area.pack_start(save_button, False, False)
        self.dialog.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)

        # initialize text entries and format plot
        self.update_daterange(self.dateselector)

        # connect the signals
        self.start_date_entry.connect('key-press-event', self.on_keypress_in_entry)
        self.end_date_entry.connect('key-press-event', self.on_keypress_in_entry)
        self.dateselector.connect('changed', self.update_daterange)
        date_update_button.connect('clicked', self.update_plot)
        save_button.connect('clicked', self.save_plot)

        # show the content
        self.dialog.show_all()

    def run(self):
        """Runs the dialog and closes it afterwards."""
        response = self.dialog.run()
        self.dialog.hide()

    # callback functions

    def update_plot(self, button):
        """Redraws the plot with the current start/end dates."""
        try:
            mindate = util.str2date(self.start_date_entry.get_text())
            maxdate = util.str2date(self.end_date_entry.get_text())
        except:
            title = _('Error: Wrong Format')
            message = _('The data entered is not in the correct format!')
            MessageDialog(type='error', title=title, message=message).run()
            return None
        if mindate >= maxdate:
            title = _('Error: Wrong Format')
            message = _('The start date has to be before the end date!')
            MessageDialog(type='error', title=title, message=message).run()
            return None
        self.plot.update_plot(mindate, maxdate)

    def update_daterange(self, dateselector):
        """Updates start and end date in the appropriate text entries
        everytime self.dateselector changes."""
        key = self.dateselector.get_active()
        start_date, end_date = get_daterange(key)
        self.start_date_entry.set_text(str(start_date))
        self.end_date_entry.set_text(str(end_date))
        self.plot.update_plot(start_date, end_date)

    def save_plot(self, button):
        """Runs the dialog to save the plot to a file."""
        SaveFileDialog(_('weight_plot.png'), ['.png', '.svg']).run(self.plot)

    def on_keypress_in_entry(self, entry, event):
        """Updates the plot when Enter is pressed."""
        if event.keyval in [gtk.keysyms.Return, gtk.keysyms.KP_Enter]:
            self.update_plot(None)

# helper functions

def get_daterange(key):
    """Returns start and end date of the plot to be created,
    depending on the current setting of self.dateselector."""
    if key == 0:
        dateoffset = timedelta(days=10)
        mindate_meas, maxdate_meas = datasets.all_datasets.get_daterange()
        if parameters.config['preferences.use_weight_plan'] \
            and parameters.config['preferences.plot_weight_plan']:
            mindate_plan, maxdate_plan = datasets.plan_datasets.get_daterange()
        else:
            mindate_plan, maxdate_plan = None, None
        mindate, maxdate = util.compare_with_possible_nones( \
            mindate_meas, maxdate_meas, mindate_plan, maxdate_plan)
        mindate -= dateoffset
        maxdate += dateoffset
    else:
        maxdate = date.today()
        if key == 1:
            # select last year
            mindate = maxdate - timedelta(days=365)
        if key == 2:
            # select last month
            mindate = maxdate - timedelta(days=31)
    return mindate, maxdate
