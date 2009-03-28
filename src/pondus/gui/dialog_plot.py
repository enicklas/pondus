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
from datetime import date, timedelta

from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg \
    as FigureCanvas

from pondus import user_data
from pondus.core import util
from pondus.core.plot import Plot
from pondus.gui.dialog_message import MessageDialog
from pondus.gui.dialog_save_file import SaveFileDialog


class PlotDialog(object):
    """Implements the dialog to plot weight versus a selected time
    range."""

    def __init__(self):
        self.dialog = gtk.Dialog(title=_('Plot Weight'))
        self.dialog.set_default_size(600,450)

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
        self.dateselector.append_text(_('Custom'))
        self.dateselector.set_active(0)
        date_selection_box.pack_start(self.dateselector, True, False)

        date_update_button = gtk.Button(label=_('Update'))
        date_selection_box.pack_end(date_update_button, False, False)
        self.dialog.vbox.pack_start(date_selection_box, False, False)

        # plot options
        plot_options_box = gtk.HBox(homogeneous=False, spacing=5)
        date_label = gtk.Label(_('Data to plot:'))
        plot_options_box.pack_start(date_label, False, False)
        self.plotselector = gtk.combo_box_new_text()
        self.plotselector.append_text(_('Weight'))
        self.plotselector.append_text(_('Body Mass Index'))
        self.plotselector.set_active(0)
        if user_data.user.height < 30:
            self.plotselector.set_sensitive(False)
        plot_options_box.pack_start(self.plotselector, False, False)
        self.smoothselector = gtk.combo_box_new_text()
        self.smoothselector.append_text(_('Both'))
        self.smoothselector.append_text(_('Raw'))
        self.smoothselector.append_text(_('Smooth'))
        self.smoothselector.set_active(0)
        plot_options_box.pack_start(self.smoothselector, False, False)
        self.plot_plan = gtk.CheckButton(_('Include Weight Plan'))
        self.plot_plan.set_active(self.plot.plot_plan)
        self.plot_plan.set_sensitive(self.plot.plot_plan)
        plot_options_box.pack_start(self.plot_plan, True, False)
        self.dialog.vbox.pack_start(plot_options_box, False, False)

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
        self.plotselector.connect('changed', self.update_plot_type)
        self.smoothselector.connect('changed', self.update_plot_smoothness)
        date_update_button.connect('clicked', self.update_plot)
        save_button.connect('clicked', self.save_plot)
        self.plot_plan.connect('toggled', self.on_toggle_plot_plan)

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
        self.plot.update_daterange(mindate, maxdate)
        self.dateselector.set_active(3)
        return None

    def update_daterange(self, dateselector):
        """Updates start and end date in the appropriate text entries
        everytime self.dateselector changes."""
        start_date, end_date = self.get_daterange()
        self.start_date_entry.set_text(str(start_date))
        self.end_date_entry.set_text(str(end_date))
        self.plot.update_daterange(start_date, end_date)

    def update_plot_type(self, plotselector):
        """Redraws the plot with the desired data (weight or bmi)."""
        key = plotselector.get_active()
        if key == 0:
            self.plot.set_plot_bmi(False)
        elif key == 1:
            self.plot.set_plot_bmi(True)
        self.plot.update_plot_type()

    def update_plot_smoothness(self, smoothselector):
        """Redraws the plot with the desired data (raw or smoothed)."""
        key = smoothselector.get_active()
        if key == 0:
            self.plot.set_plot_smooth(True)
            self.plot.set_plot_raw(True)
        elif key == 1:
            self.plot.set_plot_smooth(False)
            self.plot.set_plot_raw(True)
        elif key == 2:
            self.plot.set_plot_smooth(True)
            self.plot.set_plot_raw(False)
        self.plot.update_plot_type()

    def save_plot(self, button):
        """Runs the dialog to save the plot to a file."""
        SaveFileDialog(_('weight_plot.png'), ['.png', '.svg']).run(self.plot)

    def on_keypress_in_entry(self, entry, event):
        """Updates the plot when Enter is pressed."""
        if event.keyval in [gtk.keysyms.Return, gtk.keysyms.KP_Enter]:
            self.update_plot(None)

    def on_toggle_plot_plan(self, plot_plan_button):
        """Redraws the plot and in-/excludes the weight plan."""
        self.plot.set_plot_plan(plot_plan_button.get_active())
        self.plot.update_plot_type()

    # helper functions

    def get_daterange(self):
        """Returns start and end date of the plot to be created,
        depending on the current setting of self.dateselector."""
        key = self.dateselector.get_active()
        if key == 0:
            dateoffset = timedelta(days=10)
            mindate = self.plot.mindate_min - dateoffset
            maxdate = self.plot.maxdate_max + dateoffset
        elif key == 1:
            # select last year
            dateoffset = timedelta(days=4)
            maxdate = date.today() + dateoffset
            mindate = maxdate - timedelta(days=365) - 2*dateoffset
        elif key == 2:
            # select last month
            dateoffset = timedelta(days=1)
            maxdate = date.today() + dateoffset
            mindate = maxdate - timedelta(days=31) - 2*dateoffset
        else:
            mindate = util.str2date(self.start_date_entry.get_text())
            maxdate = util.str2date(self.end_date_entry.get_text())
        return mindate, maxdate
