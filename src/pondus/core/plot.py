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

from datetime import date, timedelta
from matplotlib.figure import Figure
from matplotlib import dates

from pondus import datasets


class Plot(object):
    """Describes the plot figure and implements methods to modify it."""
    def __init__(self):
        """Plots the weight data vs time."""
        self.get_plot_data()
        self.create_plot()
        self.format_plot()

    def get_plot_data(self):
        """Creates the datalists to be plotted."""
        datasets.all_datasets.clear_selection()
        plot_data = [(dataset.data['date'], dataset.data['weight']) \
                for dataset in datasets.all_datasets.get_selection()]
        plot_data.sort()
        self.datelist = [tup[0] for tup in plot_data]
        self.weightlist = [tup[1] for tup in plot_data]

    def create_plot(self):
        """Creates the plot and basic formatting."""
        self.figure = Figure()
        self.ax = self.figure.add_subplot(111)
        self.ax.plot_date(dates.date2num(self.datelist), \
                            self.weightlist, fmt='bo', ls='-')
        self.ax.set_ylabel(_('Weight [kg]'))
        self.ax.grid(True)

    def format_plot(self, key=0):
        """Formats the plot, i.e. sets limits, ticks, etc."""
        if key == 0:
            # select all datasets
            datasets.all_datasets.clear_selection()
            dateoffset = timedelta(days = 10)
            mindate = min(self.datelist) - dateoffset
            maxdate = max(self.datelist) + dateoffset
            daterange = maxdate - mindate
            if daterange >= timedelta(days = 700):
                majorlocator = dates.YearLocator()
                majorformatter = dates.DateFormatter("%Y")
                minorlocator = dates.MonthLocator(bymonth=(1, 4, 7, 10))
            elif daterange >= timedelta(days = 200):
                majorlocator = dates.MonthLocator(bymonth=(1, 4, 7, 10))
                majorformatter = dates.DateFormatter("%b %Y")
                minorlocator = dates.MonthLocator()
            elif daterange >= timedelta(days = 50):
                majorlocator = dates.MonthLocator()
                majorformatter = dates.DateFormatter("%b %Y")
                minorlocator = dates.WeekdayLocator(byweekday=6)
            else:
                majorlocator = dates.WeekdayLocator(byweekday=6)
                majorformatter = dates.DateFormatter("%d %b")
                minorlocator = dates.DayLocator()
        else:
            maxdate = date.today()
            if key == 1:
                # select last year
                mindate = maxdate - timedelta(days = 365)
                majorlocator = dates.MonthLocator(bymonth=(1, 4, 7, 10))
                majorformatter = dates.DateFormatter("%b %Y")
                minorlocator = dates.MonthLocator()
            if key == 2:
                # select last month
                mindate = maxdate - timedelta(days = 31)
                majorlocator = dates.WeekdayLocator(byweekday=6)
                majorformatter = dates.DateFormatter("%d %b")
                minorlocator = dates.DayLocator()
            datasets.all_datasets.select_by_date(mindate, maxdate)

        try:
            weightoffset = 0.5
            minweight = min(dataset.data['weight'] \
                    for dataset in datasets.all_datasets.get_selection()) \
                    - weightoffset
            maxweight = max(dataset.data['weight'] \
                    for dataset in datasets.all_datasets.get_selection()) \
                    + weightoffset
            self.ax.set_ylim(minweight, maxweight)
        except ValueError:
            # if no datasets in the selections, min([]) raises error
            pass

        self.ax.set_xlim(dates.date2num(mindate), \
                            dates.date2num(maxdate))
        self.ax.xaxis.set_major_locator(majorlocator)
        self.ax.xaxis.set_major_formatter(majorformatter)
        self.ax.xaxis.set_minor_locator(minorlocator)

    def update_plot(self, key):
        """Updates the plot formatting and redraws the plot."""
        self.format_plot(key)
        self.figure.canvas.draw()
