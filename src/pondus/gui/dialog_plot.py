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

from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg \
    as FigureCanvas

from pondus.core.plot import Plot


class PlotDialog(object):
    """Implements the dialog to plot weight versus a selected time
    range."""

    def __init__(self):
        self.dialog = gtk.Dialog(title='Plot Weight')
        self.dialog.set_default_size(600,400)

        # drawing area for the plot
        self.plot = Plot()
        self.canvas = FigureCanvas(self.plot.figure)
        self.dialog.vbox.set_spacing(5)
        self.dialog.vbox.pack_start(self.canvas)

        # date selection
        date_selection_box = gtk.HBox(homogeneous = False, spacing=5)

        date_label = gtk.Label('Select Date Range:')
        date_selection_box.pack_start(date_label, False, False)

        self.dateselector = gtk.combo_box_new_text()
        self.dateselector.append_text('All Time')
        self.dateselector.append_text('Last Year')
        self.dateselector.append_text('Last Month')
        self.dateselector.set_active(0)
        date_selection_box.pack_start(self.dateselector, False, False)

        date_update_button = gtk.Button(label='Update')
        date_selection_box.pack_start(date_update_button, False, False)
        self.dialog.vbox.pack_start(date_selection_box, False, False)

        # buttons in action field
        self.dialog.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)

        # connect the signals
        date_update_button.connect('clicked', self.update_plot)

        # show the content
        self.dialog.show_all()

    def run(self):
        """Runs the dialog and closes it afterwards."""
        response = self.dialog.run()
        self.dialog.hide()

    # callback functions

    def update_plot(self, button):
        key = self.dateselector.get_active()
        self.plot.update_plot(key)
