# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2007-10  Eike Nicklas <eike@ephys.de>

This program is free software licensed under the MIT license. For details
see LICENSE or http://www.opensource.org/licenses/mit-license.php
"""

from datetime import timedelta
from matplotlib.figure import Figure
from matplotlib import dates

from pondus.core import parameters
from pondus.core import util


class Plot(object):
    """Creates the weight plot and implements methods to modify it."""
    def __init__(self):
        """Initializes the plot data and creates the plot."""
        # default settings
        self.set_plot_plan(parameters.config['preferences.use_weight_plan'])
        self.set_plot_raw(True)
        self.set_plot_smooth(True)
        self.set_plot_bmi(False)
        # get plot data
        self._set_current_plot_data()
        self.get_max_daterange()
        # plot whole date range by default
        self.start_date, self.end_date = self.MINDATE, self.MAXDATE
        # create plot
        self._create_figure()
        self._plot_data()
        self._format_plot()

    # external api
    def set_plot_bmi(self, plot_bmi):
        """Sets the parameter describing whether weight or BMI is plotted."""
        self.PLOT_BMI = plot_bmi
        if self.PLOT_BMI:
            self.YLABEL = _('Body Mass Index')
        else:
            self.YLABEL = _('Weight') + ' (' + util.get_weight_unit() + ')'

    def set_plot_plan(self, plot_plan):
        """Sets the parameter describing whether the weight plan is plotted."""
        self.PLOT_PLAN = plot_plan

    def set_plot_raw(self, plot_raw):
        """Sets the parameter describing whether the actual weight data
        is plotted."""
        self.PLOT_RAW = plot_raw

    def set_plot_smooth(self, plot_smooth):
        """Sets the parameter describing whether the smoothed weight data
        is plotted."""
        self.PLOT_SMOOTH = plot_smooth

    def get_plot_plan(self):
        """Returns the parameter describing whether the weight plan is
        plotted."""
        return self.PLOT_PLAN

    def get_mindate(self):
        """Returns the minimum date in the datasets."""
        return self.MINDATE

    def get_maxdate(self):
        """Returns the maximum date in the datasets."""
        return self.MAXDATE

    def set_plotrange(self, start_date, end_date):
        """Updates the axis scaling of the plot."""
        self.start_date, self.end_date = start_date, end_date
        self._format_plot()
        self.figure.canvas.draw()

    def update_plot(self):
        """Updates the plot with the current settings."""
        # clear old plot data...
        self.ax.clear()
        # ...and create the new data
        self._set_current_plot_data()
        self._plot_data()
        self._format_plot()
        self.figure.canvas.draw()

    def save_to_file(self, filename):
        """Saves the plot to filename. The filename's ending must be
        a valid format to save to."""
        print _('Saving plot to'), filename
        self.figure.savefig(filename, format=filename[-3:])

    def get_max_daterange(self):
        """Sets the minimum and the maximum date in the available data."""
        mindates = []
        maxdates = []
        if self.plot_data_measurement:
            mindates.append(self.plot_data_measurement[0][0])
            maxdates.append(self.plot_data_measurement[-1][0])
        if self.plot_data_plan:
            mindates.append(self.plot_data_plan[0][0])
            maxdates.append(self.plot_data_plan[-1][0])
        # initially, mindates can not be empty, but can that happen later,
        # if only plan data is available in PLOT_PLAN is then set to False
        if mindates:
            self.MINDATE = min(mindates)
            self.MAXDATE = max(maxdates)

    # internal helper methods
    def _set_current_plot_data(self):
        """Updates the plot data according to the current settings."""
        self.plot_data_measurement = \
                        self._get_plot_data(parameters.user.measurements)
        # for performance improvements, only get plan data if really needed
        if self.PLOT_PLAN:
            self.plot_data_plan = self._get_plot_data(parameters.user.plan)
        else:
            self.plot_data_plan = []
        if self.PLOT_SMOOTH:
            self.plot_data_measurement = \
                            _smooth_data(self.plot_data_measurement)

    def _get_plot_data(self, datasets):
        """Returns the list of datatuples to be plotted."""
        if self.PLOT_BMI:
            data = [(dataset.date,
                    util.bmi(dataset.weight, parameters.user.height))
                    for dataset in datasets]
        elif parameters.config['preferences.unit_system'] == 'imperial':
            data = [(dataset.date, dataset.weight_lbs)
                    for dataset in datasets]
        else:
            data = [(dataset.date, dataset.weight) for dataset in datasets]
        data.sort()
        return data

    def _create_figure(self):
        """Creates the figure object containing the plot."""
        self.figure = Figure()
        self.ax = self.figure.add_subplot(111)

    def _plot_data(self):
        """Plots the data."""
        if self.PLOT_RAW and self.plot_data_measurement:
            xvalues = [tup[0] for tup in self.plot_data_measurement]
            yvalues = [tup[1] for tup in self.plot_data_measurement]
            self.ax.plot_date(dates.date2num(xvalues), yvalues,
                            fmt='bo-', ms=4.0)
        if self.PLOT_SMOOTH and self.plot_data_measurement:
            xvalues = [tup[0] for tup in self.plot_data_measurement]
            yvalues = [tup[2] for tup in self.plot_data_measurement]
            self.ax.plot_date(dates.date2num(xvalues), yvalues,
                            fmt='co-', ms=4.0)
        if self.PLOT_PLAN and self.plot_data_plan:
            xvalues = [tup[0] for tup in self.plot_data_plan]
            yvalues = [tup[1] for tup in self.plot_data_plan]
            self.ax.plot_date(dates.date2num(xvalues), yvalues,
                            fmt='ro-', ms=4.0)

    def _format_plot(self):
        """Formats the plot, i.e. scales axes, sets ticks, etc."""
        # enable grid
        self.ax.grid(True)
        # format x-axis
        daterange = self.end_date - self.start_date
        majorlocator, majorformatter, minorlocator = _get_locators(daterange)
        self.ax.set_xlim(
                dates.date2num(self.start_date), dates.date2num(self.end_date))
        self.ax.xaxis.set_major_locator(majorlocator)
        self.ax.xaxis.set_major_formatter(majorformatter)
        self.ax.xaxis.set_minor_locator(minorlocator)
        # format y-axis
        y_min, y_max = self._get_ylimits()
        if y_min is not None:
            self.ax.set_ylim(y_min, y_max)
        # set label on y-axis
        self.ax.set_ylabel(self.YLABEL)

    def _get_ylimits(self):
        """Returns the minimum and the maximum y-value in the current date
        range. Offsets are used for proper axis scaling."""
        if self.PLOT_BMI:
            y_offset = 0.1
        else:
            y_offset = 0.5
        y_min, y_max = self._get_yrange(self.plot_data_measurement)
        if self.PLOT_PLAN:
            y_min_plan, y_max_plan = self._get_yrange(self.plot_data_plan)
            y_min = util.nonemin([y_min, y_min_plan])
            y_max = util.nonemax([y_max, y_max_plan])
        # y_min, y_max can be None if no datasets in selected daterange
        if y_min is not None:
            y_min -= y_offset
            y_max += y_offset
        return y_min, y_max

    def _get_yrange(self, datasets):
        """Returns the minimum and the maximum y-value in the given datasets.
        Returns None, None if no measurements exist in the current date
        range."""
        try:
            y_min = min(dataset[1] for dataset in datasets
                        if self.start_date <= dataset[0] <= self.end_date)
            y_max = max(dataset[1] for dataset in datasets
                        if self.start_date <= dataset[0] <= self.end_date)
            return y_min, y_max
        except ValueError:
            return None, None


# internal helper functions
def _smooth_data(data):
    """Computes exponential central moving average."""
    # attenuation factor reducing the weight of neighboring datasets
    alpha = 0.8
    # number of datapoints to average
    avg_datapoints = 3
    smooth_data = []
    for i in xrange(0, len(data)):
        deltas = []
        datapoints = []
        for j in xrange(i-avg_datapoints, i+avg_datapoints+1):
            try:
                delta = abs((data[j][0] - data[i][0]).days)
                deltas.append(delta)
                datapoints.append(data[j][1])
            except IndexError:
                pass
        weights = []
        for delta in deltas:
            weights.append(alpha**(delta))
        weighted_data = [datapoints[k] * weights[k]
                            for k in xrange(len(datapoints))]
        weighted_average = sum(weighted_data)/sum(weights)
        smooth_data.append((data[i][0], data[i][1], weighted_average))
    return smooth_data

def _get_locators(daterange):
    """Returns sane locators and formatters for the given daterange."""
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
