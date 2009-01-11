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

from datetime import timedelta
from matplotlib.figure import Figure
from matplotlib import dates

from pondus import user_data
from pondus import parameters
from pondus.core import util


class Plot(object):
    """Describes the plot figure and implements methods to modify it."""
    def __init__(self):
        """Plots the weight data vs time."""
        self.plot_plan = parameters.config['preferences.use_weight_plan']
        self.plot_smooth = True
        self.plot_raw = True
        self.plot_bmi = False
        self.alpha = 0.1
        self.figure = Figure()
        self.ax = self.figure.add_subplot(111)
        self.ax.grid(True)
        self.get_plot_data()
        self.mindate = self.mindate_min
        self.maxdate = self.maxdate_max
        self.create_plot()

    def set_daterange(self, mindate, maxdate):
        """Sets the desired daterange of the plot."""
        self.mindate = mindate
        self.maxdate = maxdate

    def set_plot_bmi(self, plot_bmi):
        """Sets the parameter describing whether weight or BMI is
        plotted."""
        self.plot_bmi = plot_bmi

    def set_plot_plan(self, plot_plan):
        """Sets the parameter describing whether the weight plan is
        plotted."""
        self.plot_plan = plot_plan

    def set_plot_smooth(self, plot_smooth):
        """Sets the parameter describing whether we want to plot
        the exponential average."""
        self.plot_smooth = plot_smooth

    def set_plot_raw(self, plot_raw):
        """Sets the parameter describing whether we want to plot
        the actual weights."""
        self.plot_raw = plot_raw

    def create_plot(self):
        """Creates the plot and basic formatting."""
        xlist_meas = [tup[0] for tup in self.plot_data_meas]
        ylist_meas = [tup[1] for tup in self.plot_data_meas]
        alist_meas = [tup[2] for tup in self.plot_data_meas]
        xlist_plan = [tup[0] for tup in self.plot_data_plan]
        ylist_plan = [tup[1] for tup in self.plot_data_plan]
        alist_plan = [tup[2] for tup in self.plot_data_plan]
        if len(xlist_meas) != 0:
            if self.plot_raw:
                self.ax.plot_date(dates.date2num(xlist_meas), ylist_meas, \
                                fmt='bo-', ms=4.0)
            if self.plot_smooth:
                self.ax.plot_date(dates.date2num(xlist_meas), alist_meas, \
                                fmt='co-', ms=4.0)
        if len(xlist_plan) != 0 and self.plot_plan:
            if self.plot_raw:
                self.ax.plot_date(dates.date2num(xlist_plan), ylist_plan, \
                                fmt='ro-', ms=4.0)
            if self.plot_smooth:
                self.ax.plot_date(dates.date2num(xlist_plan), alist_plan, \
                                fmt='yo-', ms=4.0)
        if self.plot_bmi:
            ylabel = _('Body Mass Index')
        else:
            ylabel = _('Weight') + ' (' + util.get_weight_unit() + ')'
        self.ax.set_ylabel(ylabel)

    def format_plot(self):
        """Formats the plot, i.e. sets limits, ticks, etc."""
        daterange = self.maxdate - self.mindate
        majorlocator, majorformatter, minorlocator = get_locators(daterange)

        y_min, y_max = self.get_yrange()
        if y_min is not None:
            self.ax.set_ylim(y_min, y_max)

        self.ax.set_xlim(dates.date2num(self.mindate), \
                         dates.date2num(self.maxdate))
        self.ax.xaxis.set_major_locator(majorlocator)
        self.ax.xaxis.set_major_formatter(majorformatter)
        self.ax.xaxis.set_minor_locator(minorlocator)

    def update_daterange(self, mindate, maxdate):
        """Updates the plot formatting and redraws the plot."""
        self.set_daterange(mindate, maxdate)
        self.format_plot()
        self.figure.canvas.draw()

    def update_plot_type(self):
        self.ax.lines = []
        self.get_plot_data()
        self.create_plot()
        self.format_plot()
        self.figure.canvas.draw()

    def save_to_file(self, filename):
        """Saves the plot to filename. The filename's ending must be
        a valid format to save to."""
        print _('Saving plot to'), filename
        self.figure.savefig(filename, format=filename[-3:])

    def get_yrange(self):
        """Returns the minimum and the maximum y-value in the given date
        range."""
        if self.plot_bmi:
            y_offset = 0.1
        else:
            y_offset = 0.5
        y_min_meas, y_max_meas = self.get_yrange_data(self.plot_data_meas)
        y_min_plan, y_max_plan = self.get_yrange_data(self.plot_data_plan)
        y_min, y_max = util.compare_with_possible_nones( \
            y_min_meas, y_max_meas, y_min_plan, y_max_plan)
        # y_min, y_max can be None if no datasets in selected daterange
        if y_min is not None:
            y_min -= y_offset
            y_max += y_offset
        return y_min, y_max

    def get_yrange_data(self, datasets):
        """Returns the minimum and the maximum y-value in the plot data.
        Returns None, None if no measurements exist in the chosen date
        range."""
        try:
            minweight = min(dataset[1] \
                for dataset in datasets \
                if self.mindate <= dataset[0] <= self.maxdate)
            maxweight = max(dataset[1] \
                for dataset in datasets \
                if self.mindate <= dataset[0] <= self.maxdate)
            return minweight, maxweight
        except ValueError:
            return None, None

    def get_max_daterange(self):
        """Returns the minimum and the maximum date in the available
        data."""
        try:
            mindate_meas = self.plot_data_meas[0][0]
            maxdate_meas = self.plot_data_meas[-1][0]
        except IndexError:
            mindate_meas = None
            maxdate_meas = None
        try:
            mindate_plan = self.plot_data_plan[0][0]
            maxdate_plan = self.plot_data_plan[-1][0]
        except IndexError:
            mindate_plan = None
            maxdate_plan = None
        mindate, maxdate = util.compare_with_possible_nones( \
            mindate_meas, maxdate_meas, mindate_plan, maxdate_plan)
        return mindate, maxdate

    def get_plot_data(self):
        """Gets the data to be plotted."""
        self.plot_data_meas = self.get_datasets(user_data.user.measurements)
        if self.plot_plan:
            self.plot_data_plan = self.get_datasets(user_data.user.plan)
        else:
            self.plot_data_plan = []
        self.mindate_min, self.maxdate_max = self.get_max_daterange()

    def get_datasets(self, datasets):
        """Returns the list of datatuples to be plotted."""
        if self.plot_bmi:
            data = [(dataset.get('date'), \
                util.bmi(dataset.get('weight'), user_data.user.height)) \
                for dataset in datasets]
        else:
            if parameters.config['preferences.unit_system'] == 'metric':
                data = [(dataset.get('date'), dataset.get('weight')) \
                        for dataset in datasets]
            else:
                data = [(dataset.get('date'), \
                        util.kg_to_lbs(dataset.get('weight'))) \
                        for dataset in datasets]
        data.sort()
        # Compute exponential moving average
        current = data[0][1]
        data[0] = (data[0][0], data[0][1], current)
        for i in xrange(1, len(data)):
            delta = (data[i][0] - data[i-1][0]).days
            current = current + self.alpha**(1.0/delta)*(data[i][1]-current)
            data[i] = (data[i][0], data[i][1], current)
        return data

def get_locators(daterange):
    """Returns sane locators and formatters for the given
    daterange."""
    if daterange >= timedelta(days=8000):
        majorlocator = dates.YearLocator(10)
        majorformatter = dates.DateFormatter("%Y")
        minorlocator = dates.YearLocator(2)
    elif daterange >= timedelta(days=4000):
        majorlocator = dates.YearLocator(2)
        majorformatter = dates.DateFormatter("%Y")
        minorlocator = dates.YearLocator()
    elif daterange >= timedelta(days = 700):
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
    return majorlocator, majorformatter, minorlocator
