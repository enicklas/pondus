# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2007-10  Eike Nicklas <eike@ephys.de>

This program is free software licensed under the MIT license. For details
see LICENSE or http://www.opensource.org/licenses/mit-license.php
"""

import gtk
from datetime import date, timedelta

from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg \
    as FigureCanvas

from pondus.core import parameters
from pondus.core import util
from pondus.core.plot import Plot
from pondus.gui.dialog_message import MessageDialog
from pondus.gui.dialog_save_file import SaveFileDialog


class PlotDialog(object):
    """Implements the dialog to plot weight versus a selected time
    range."""

    def __init__(self):
        self.dialog = gtk.Dialog(title=_('Plot Weight'))
        self.dialog.set_default_size(600, 450)

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
        self.start_date_entry.set_tooltip_text(_('Start date'))
        date_selection_box.pack_start(self.start_date_entry, False, False)

        date_selection_box.pack_start(gtk.Label('-'), False, False)

        self.end_date_entry = gtk.Entry()
        self.end_date_entry.set_width_chars(10)
        self.end_date_entry.set_tooltip_text(_('End date'))
        date_selection_box.pack_start(self.end_date_entry, False, False)

        self.dateselector = gtk.combo_box_new_text()
        self.dateselector.set_tooltip_text(
                    _('Select date range of plot'))
        self.dateselector.append_text(_('All Time'))
        self.dateselector.append_text(_('Last Year'))
        self.dateselector.append_text(_('Last 3 Months'))
        self.dateselector.append_text(_('Last Month'))
        self.dateselector.append_text(_('Custom'))
        self.set_dateselector_default()
        date_selection_box.pack_start(self.dateselector, False, False)
        self.dialog.vbox.pack_start(date_selection_box, False, False)

        # plot options
        plot_options_box = gtk.HBox(homogeneous=False, spacing=5)
        date_label = gtk.Label(_('Data to plot:'))
        plot_options_box.pack_start(date_label, False, False)
        self.plotselector = gtk.combo_box_new_text()
        self.plotselector.append_text(_('Weight'))
        self.plotselector.append_text(_('Body Mass Index'))
        self.plotselector.set_active(0)
        if parameters.user.height < 30:
            self.plotselector.set_sensitive(False)
            self.plotselector.set_tooltip_text(_('To plot your BMI, \
you need to enter your height in the preferences dialog.'))
        plot_options_box.pack_start(self.plotselector, False, False)
        self.smoothselector = gtk.combo_box_new_text()
        self.smoothselector.append_text(_('Raw and Smooth'))
        self.smoothselector.append_text(_('Raw'))
        self.smoothselector.append_text(_('Smooth'))
        self.smoothselector.set_active(0)
        plot_options_box.pack_start(self.smoothselector, False, False)
        self.plot_plan = gtk.CheckButton(_('Include Weight Plan'))
        self.plot_plan.set_active(self.plot.get_plot_plan())
        self.plot_plan.set_sensitive(self.plot.get_plot_plan())
        if not self.plot.get_plot_plan():
            self.plot_plan.set_tooltip_text(_('The weight planner can be \
enabled in the preferences dialog.'))
        plot_options_box.pack_start(self.plot_plan, True, False)
        self.dialog.vbox.pack_start(plot_options_box, False, False)

        # buttons in action field
        save_button = gtk.Button(label=_('Save Plot'))
        self.dialog.action_area.pack_start(save_button, False, False)
        self.dialog.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)

        # initialize text entries and format plot
        self.update_daterange(self.dateselector)

        # connect the signals
        self.start_date_entry.connect(
                        'key-press-event', self.on_keypress_in_entry)
        self.end_date_entry.connect(
                        'key-press-event', self.on_keypress_in_entry)
        self.dateselector.connect('changed', self.update_daterange)
        self.plotselector.connect('changed', self.update_plot_type)
        self.smoothselector.connect('changed', self.update_plot_smoothness)
        save_button.connect('clicked', self.save_plot)
        self.plot_plan.connect('toggled', self.on_toggle_plot_plan)

        # show the content
        self.dialog.show_all()

    def run(self):
        """Runs the dialog and closes it afterwards."""
        self.dialog.run()
        self.dialog.hide()

    # callback functions

    def update_plot(self, button):
        """Redraws the plot with the current start/end dates."""
        try:
            mindate = util.str2date(self.start_date_entry.get_text())
            maxdate = util.str2date(self.end_date_entry.get_text())
        except ValueError:
            title = _('Error: Wrong Format')
            message = _('The data entered is not in the correct format!')
            MessageDialog(type_='error', title=title, message=message).run()
            return
        if mindate >= maxdate:
            title = _('Error: Wrong Format')
            message = _('The start date has to be before the end date!')
            MessageDialog(type_='error', title=title, message=message).run()
            return
        self.plot.set_plotrange(mindate, maxdate)
        self.dateselector.set_active(4)

    def update_daterange(self, dateselector):
        """Updates start and end date in the appropriate text entries
        everytime self.dateselector changes."""
        start_date, end_date = self.get_daterange()
        self.start_date_entry.set_text(str(start_date))
        self.end_date_entry.set_text(str(end_date))
        self.plot.set_plotrange(start_date, end_date)

    def update_plot_type(self, plotselector):
        """Redraws the plot with the desired data (weight or bmi)."""
        key = plotselector.get_active()
        if key == 0:
            self.plot.set_plot_bmi(False)
        elif key == 1:
            self.plot.set_plot_bmi(True)
        self.plot.update_plot()

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
        self.plot.update_plot()

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
        self.plot.update_plot()
        self.plot.get_max_daterange()
        # if daterange is 'All Time', rescale date axis
        if self.dateselector.get_active() == 0:
            self.update_daterange(self.dateselector)


    # helper methods

    def get_daterange(self):
        """Returns start and end date of the plot to be created,
        depending on the current setting of self.dateselector."""
        key = self.dateselector.get_active()
        if key == 0:
            dateoffset = timedelta(days=10)
            mindate = self.plot.get_mindate() - dateoffset
            maxdate = self.plot.get_maxdate() + dateoffset
        elif key == 1:
            # select last year
            dateoffset = timedelta(days=4)
            maxdate = date.today() + dateoffset
            mindate = maxdate - timedelta(days=365) - 2*dateoffset
        elif key == 2:
            # select last 3 months
            dateoffset = timedelta(days=2)
            maxdate = date.today() + dateoffset
            mindate = maxdate - timedelta(days=91) - 2*dateoffset
        elif key == 3:
            # select last month
            dateoffset = timedelta(days=1)
            maxdate = date.today() + dateoffset
            mindate = maxdate - timedelta(days=31) - 2*dateoffset
        else:
            mindate = util.str2date(self.start_date_entry.get_text())
            maxdate = util.str2date(self.end_date_entry.get_text())
        return mindate, maxdate

    def set_dateselector_default(self):
        """Sets the default daterange of the plot to 3 months, if sensible."""
        if (self.plot.get_mindate() > date.today() - timedelta(days=91)
            or self.plot.get_maxdate() < date.today() - timedelta(days=91)):
            self.dateselector.set_active(0)
        else:
            self.dateselector.set_active(2)
