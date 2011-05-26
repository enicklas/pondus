# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2007-11  Eike Nicklas <eike@ephys.de>

This program is free software licensed under the MIT license. For details
see LICENSE or http://www.opensource.org/licenses/mit-license.php
"""

import pygtk
pygtk.require('2.0')

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
        # start date
        self.start_date_entry = gtk.Entry()
        self.start_date_entry.set_width_chars(10)
        self.start_date_entry.set_tooltip_text(_('Start date'))
        date_selection_box.pack_start(self.start_date_entry, False, False)
        date_selection_box.pack_start(gtk.Label('-'), False, False)
        # end date
        self.end_date_entry = gtk.Entry()
        self.end_date_entry.set_width_chars(10)
        self.end_date_entry.set_tooltip_text(_('End date'))
        date_selection_box.pack_start(self.end_date_entry, False, False)
        # preset date ranges
        self.dateselector = gtk.combo_box_new_text()
        self.dateselector.set_tooltip_text(
                    _('Select date range of plot'))
        self.dateselector.append_text(_('All Time'))
        self.dateselector.append_text(_('Last Year'))
        self.dateselector.append_text(_('Last 6 Months'))
        self.dateselector.append_text(_('Last Month'))
        self.dateselector.append_text(_('Custom'))
        self.set_dateselector_default()
        date_selection_box.pack_start(self.dateselector, False, False)
        self.dialog.vbox.pack_start(date_selection_box, False, False)
        # select data to plot
        plot_options_box = gtk.HBox(homogeneous=False, spacing=5)
        # left data type selector
        data_label_left = gtk.Label(_('Data Left:'))
        plot_options_box.pack_start(data_label_left, False, False)
        self.plotselector_left = gtk.combo_box_new_text()
        self.plotselector_left.set_name('left')
        self.plotselector_left.append_text(_('Weight'))
        self.plotselector_keys = ['weight']
        if parameters.config['preferences.use_bodyfat']:
            self.plotselector_left.append_text(_('Bodyfat'))
            self.plotselector_keys.append('bodyfat')
        if parameters.config['preferences.use_muscle']:
            self.plotselector_left.append_text(_('Muscle'))
            self.plotselector_keys.append('muscle')
        if parameters.config['preferences.use_water']:
            self.plotselector_left.append_text(_('Water'))
            self.plotselector_keys.append('water')
        if parameters.user.height < 30:
            self.plotselector_left.set_tooltip_text(_('To plot your BMI, \
you need to enter your height in the preferences dialog.'))
        else:
            self.plotselector_left.append_text(_('Body Mass Index'))
            self.plotselector_keys.append('bmi')
        self.plotselector_left.set_active(0)
        plot_options_box.pack_start(self.plotselector_left, False, False)
        # right data type selector
        data_label_right = gtk.Label(_('Right:'))
        plot_options_box.pack_start(data_label_right, False, False)
        self.plotselector_right = gtk.combo_box_new_text()
        self.plotselector_right.set_name('right')
        self.plotselector_right.append_text(_('Weight'))
        if parameters.config['preferences.use_bodyfat']:
            self.plotselector_right.append_text(_('Bodyfat'))
            self.plotselector_right.set_active(1)
        if parameters.config['preferences.use_muscle']:
            self.plotselector_right.append_text(_('Muscle'))
        if parameters.config['preferences.use_water']:
            self.plotselector_right.append_text(_('Water'))
        if parameters.user.height < 30:
            self.plotselector_right.set_tooltip_text(_('To plot your BMI, \
you need to enter your height in the preferences dialog.'))
        else:
            self.plotselector_right.append_text(_('Body Mass Index'))
        self.plotselector_right.append_text(_('None'))
        self.plotselector_keys.append(None)
        if not parameters.config['preferences.use_bodyfat']:
            self.plotselector_right.set_active( \
                    self.plotselector_keys.index(None))
        plot_options_box.pack_start(self.plotselector_right, False, False)
        # smooth data checkbox
        self.smooth_data = gtk.CheckButton(_('Smooth'))
        self.smooth_data.set_active(self.plot.get_smooth())
        plot_options_box.pack_start(self.smooth_data, True, False)
        # plot plan checkbox
        self.plot_plan = gtk.CheckButton(_('Show Plan'))
        self.plot_plan.set_active(self.plot.get_show_plan())
        self.plot_plan.set_sensitive(self.plot.get_show_plan())
        if not self.plot.get_show_plan():
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
        self.plotselector_left.connect('changed', self.update_plot_type)
        self.plotselector_right.connect('changed', self.update_plot_type)
        self.smooth_data.connect('toggled', self.on_toggle_smooth_data)
        self.plot_plan.connect('toggled', self.on_toggle_plot_plan)
        save_button.connect('clicked', self.save_plot)
        # show the content
        self.dialog.show_all()

    def run(self):
        """Runs the dialog and closes it afterwards."""
        self.dialog.run()
        self.dialog.hide()

    # callback functions

    def set_custom_date_range(self):
        """Redraws the plot with the current start/end dates."""
        try:
            start_date = util.str2date(self.start_date_entry.get_text())
            end_date = util.str2date(self.end_date_entry.get_text())
        except ValueError:
            title = _('Error: Wrong Format')
            message = _('The data entered is not in the correct format!')
            MessageDialog(type_='error', title=title, message=message).run()
            return
        if start_date >= end_date:
            title = _('Error: Wrong Format')
            message = _('The start date has to be before the end date!')
            MessageDialog(type_='error', title=title, message=message).run()
            return
        self.plot.set_date_range(start_date, end_date)
        self.dateselector.set_active(4)

    def update_daterange(self, dateselector):
        """Updates start and end date in the appropriate text entries
        everytime self.dateselector changes."""
        start_date, end_date = self.get_daterange()
        self.start_date_entry.set_text(str(start_date))
        self.end_date_entry.set_text(str(end_date))
        self.plot.set_date_range(start_date, end_date)

    def update_plot_type(self, plotselector):
        """Redraws the plot with the desired data (weight or bmi)."""
        if plotselector.get_name() == 'left':
            set_type_function = self.plot.set_left_type
        elif plotselector.get_name() == 'right':
            set_type_function = self.plot.set_right_type
        key = plotselector.get_active()
        set_type_function(self.plotselector_keys[key])
        self.update_daterange(self.dateselector)

    def on_toggle_smooth_data(self, smooth_data_button):
        """Redraws the plot with the desired data (raw or smoothed)."""
        self.plot.set_smooth(smooth_data_button.get_active())

    def save_plot(self, button):
        """Runs the dialog to save the plot to a file."""
        SaveFileDialog(_('weight_plot.png'), ['.png', '.svg']).run(self.plot)

    def on_keypress_in_entry(self, entry, event):
        """Updates the plot when Enter is pressed."""
        if event.keyval in [gtk.keysyms.Return, gtk.keysyms.KP_Enter]:
            self.set_custom_date_range()

    def on_toggle_plot_plan(self, plot_plan_button):
        """Redraws the plot and in-/excludes the weight plan."""
        self.plot.set_show_plan(plot_plan_button.get_active())
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
            # select last 6 months
            dateoffset = timedelta(days=2)
            maxdate = date.today() + dateoffset
            mindate = maxdate - timedelta(days=182) - 2*dateoffset
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
        """Sets the default daterange of the plot to last year, if sensible,
        and to 'All Time' otherwise."""
        if (self.plot.get_mindate() > date.today() - timedelta(days=365)
            or self.plot.get_maxdate() < date.today() - timedelta(days=365)):
            self.dateselector.set_active(0)
        else:
            self.dateselector.set_active(1)
