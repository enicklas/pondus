# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2007-11  Eike Nicklas <eike@ephys.de>

This program is free software licensed under the MIT license. For details
see LICENSE or http://www.opensource.org/licenses/mit-license.php
"""

from datetime import timedelta
from matplotlib.figure import Figure
from matplotlib import dates

from pondus.core import parameters
from pondus.core import util
from pondus.core.logger import logger


class Plot(object):
    """Creates the weight plot and implements methods to modify it."""
    ylabels = {
            'weight': _('Weight') + ' (' + util.get_weight_unit() + ')',
            'bmi': _('Body Mass Index'),
            'bodyfat': _('Bodyfat (%)'),
            None: ''
            }
    show_plan = False
    smooth = False
    left_datatype = None
    left_data = []
    left_plan = []
    right_datatype = None
    right_data = []
    right_plan = []

    def __init__(self):
        """Initializes the plot data and creates the plot."""
        # default settings
        self.show_plan = parameters.config['preferences.use_weight_plan']
        self.smooth = False
        self.left_datatype = 'weight'
        if parameters.config['preferences.use_bodyfat']:
            self.right_datatype = 'bodyfat'
        # get plot data
        self._update_plot_data()
        self._get_max_daterange()
        # plot whole date range by default
        self.start_date, self.end_date = self.mindate, self.maxdate
        # create plot
        self._create_figure()
        self._plot_data()
        self._format_plot()

    # external api
    def set_show_plan(self, show_plan):
        """Sets the parameter describing whether the weight plan is plotted
        and updates the plot."""
        self.show_plan = show_plan
        self._get_max_daterange()
        self._update_plot()

    def set_smooth(self, smooth):
        """Sets the parameter describing whether the plot data should be
        smoothed and updates the plot"""
        self.smooth = smooth
        self._update_plot_data()
        self._update_plot()

    def get_show_plan(self):
        """Returns the parameter describing whether the weight plan is
        plotted."""
        return self.show_plan

    def get_smooth(self):
        """Returns the parameter describing whether the data is smoothed."""
        return self.smooth

    def get_mindate(self):
        """Returns the minimum date in the datasets."""
        return self.mindate

    def get_maxdate(self):
        """Returns the maximum date in the datasets."""
        return self.maxdate

    def set_left_type(self, datatype):
        """Sets the data type plotted on the left y-axis and updates
        the plot."""
        self.left_datatype = datatype
        self._update_left_data()
        self._get_max_daterange()
        self._update_plot()

    def set_right_type(self, datatype):
        """Sets the data type plotted on the right y-axis and updates
        the plot."""
        self.right_datatype = datatype
        self._update_right_data()
        self._get_max_daterange()
        self._update_plot()

    def set_date_range(self, start_date, end_date):
        """Updates the range of the x-axis."""
        self.start_date, self.end_date = start_date, end_date
        self._format_plot()
        self.figure.canvas.draw()

    def save_to_file(self, filename):
        """Saves the plot to filename. The filename's ending must be
        a valid format to save to."""
        logger.info(_('Saving plot to %s'), filename)
        self.figure.savefig(filename, format=filename[-3:])

    # internal helper methods
    def _update_plot_data(self):
        """Update all plot data."""
        self._update_left_data()
        self._update_right_data()

    def _update_left_data(self):
        """Update the data plotted on the left y-axis."""
        self.left_data = self._get_plot_data(parameters.user.measurements, \
                    self.left_datatype)
        self.left_plan = self._get_plot_data(parameters.user.plan, \
                    self.left_datatype)
        if self.smooth and len(self.left_data) > 0:
            self.left_data = _smooth_data(self.left_data)

    def _update_right_data(self):
        """Update the data plotted on the right y-axis."""
        self.right_data = self._get_plot_data(parameters.user.measurements, \
                    self.right_datatype)
        self.right_plan = self._get_plot_data(parameters.user.plan, \
                    self.right_datatype)
        if self.smooth and len(self.right_data) > 0:
            self.right_data = _smooth_data(self.right_data)

    def _get_plot_data(self, datasets, datatype):
        """Returns the list of datatuples to be plotted."""
        if datatype == 'weight':
            if parameters.config['preferences.unit_system'] == 'imperial':
                return sorted((dataset.date, dataset.weight_lbs)
                        for dataset in datasets)
            else:
                return sorted((dataset.date, dataset.weight)
                        for dataset in datasets)
        elif datatype == 'bmi':
            return sorted((dataset.date,
                    util.bmi(dataset.weight, parameters.user.height))
                    for dataset in datasets)
        elif datatype == 'bodyfat':
            return sorted((dataset.date, dataset.bodyfat)
                    for dataset in datasets if dataset.bodyfat is not None)
        elif datatype is None:
            return []

    def _create_figure(self):
        """Creates the figure object containing the plot."""
        self.figure = Figure()
        self.ax_left = self.figure.add_subplot(111)
        self.ax_right = self.ax_left.twinx()

    def _update_plot(self):
        """Updates the plot with the current settings."""
        # clear old plot data...
        self.ax_left.clear()
        self.ax_right.clear()
        # ...and create the new data
        self._plot_data()
        self._format_plot()
        self.figure.canvas.draw()

    def _plot_data(self):
        """Plots the data."""
        if self.left_data:
            xvalues = [tup[0] for tup in self.left_data]
            yvalues = [tup[1] for tup in self.left_data]
            self.ax_left.plot_date(dates.date2num(xvalues), yvalues,
                            fmt='bo-', ms=4.0)
        if self.left_plan and self.show_plan:
            xvalues = [tup[0] for tup in self.left_plan]
            yvalues = [tup[1] for tup in self.left_plan]
            self.ax_left.plot_date(dates.date2num(xvalues), yvalues,
                            fmt='ro--', ms=4.0)
        if self.right_data:
            xvalues = [tup[0] for tup in self.right_data]
            yvalues = [tup[1] for tup in self.right_data]
            self.ax_right.plot_date(dates.date2num(xvalues), yvalues,
                            fmt='go-', ms=4.0)
        if self.right_plan and self.show_plan:
            xvalues = [tup[0] for tup in self.right_plan]
            yvalues = [tup[1] for tup in self.right_plan]
            self.ax_right.plot_date(dates.date2num(xvalues), yvalues,
                            fmt='yo--', ms=4.0)

    def _format_plot(self):
        """Formats the plot, i.e. scales axes, sets ticks, etc."""
        # enable grid
        self.ax_left.grid(True)
        # format x-axis
        daterange = self.end_date - self.start_date
        majorlocator, majorformatter, minorlocator = _get_locators(daterange)
        self.ax_left.set_xlim(
                dates.date2num(self.start_date), dates.date2num(self.end_date))
        self.ax_left.xaxis.set_major_locator(majorlocator)
        self.ax_left.xaxis.set_major_formatter(majorformatter)
        self.ax_left.xaxis.set_minor_locator(minorlocator)
        # format y-axis
        y_min, y_max = self._get_ylimits(yaxis='left')
        if y_min is not None:
            self.ax_left.set_visible(True)
            self.ax_left.set_ylim(y_min, y_max)
        else:
            self.ax_left.set_visible(False)
        y_min, y_max = self._get_ylimits(yaxis='right')
        if y_min is not None:
            self.ax_right.set_visible(True)
            self.ax_right.set_ylim(y_min, y_max)
        else:
            self.ax_right.set_visible(False)
        # set label on y-axis
        self.ax_left.set_ylabel(self.ylabels[self.left_datatype])
        self.ax_right.set_ylabel(self.ylabels[self.right_datatype])

    def _get_ylimits(self, yaxis):
        """Returns the minimum and the maximum y-value in the current date
        range. Offsets are used for proper axis scaling."""
        if yaxis == 'left':
            datatype = self.left_datatype
            data_meas = self.left_data
            data_plan = self.left_plan
        if yaxis == 'right':
            datatype = self.right_datatype
            data_meas = self.right_data
            data_plan = self.right_plan
        if datatype == 'bmi':
            y_offset = 0.1
        else:
            y_offset = 0.5
        y_min, y_max = self._get_yrange(data_meas)
        if self.show_plan:
            y_min_plan, y_max_plan = self._get_yrange(data_plan)
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

    def _get_max_daterange(self):
        """Sets the minimum and the maximum date in the available data."""
        mindates = []
        maxdates = []
        if self.left_data:
            mindates.append(self.left_data[0][0])
            maxdates.append(self.left_data[-1][0])
        if self.left_plan and self.show_plan:
            mindates.append(self.left_plan[0][0])
            maxdates.append(self.left_plan[-1][0])
        if self.right_data:
            mindates.append(self.right_data[0][0])
            maxdates.append(self.right_data[-1][0])
        if self.right_plan and self.show_plan:
            mindates.append(self.right_plan[0][0])
            maxdates.append(self.right_plan[-1][0])
        # initially, mindates can not be empty, but can that happen later,
        # if only plan data is available and show_plan is then set to False
        if mindates:
            self.mindate = min(mindates)
            self.maxdate = max(maxdates)


# internal helper functions
def _smooth_data(data):
    """Computes exponential central moving average."""
    # attenuation factor reducing the weight of neighboring datasets
    alpha = 0.8
    # number of datapoints to average
    avg_datapoints = 3
    smooth_data = []
    for i in xrange(0, len(data)):
        weights = []
        weighted_data = []
        for j in xrange(i-avg_datapoints, i+avg_datapoints+1):
            try:
                delta = abs((data[j][0] - data[i][0]).days)
                weight = alpha**delta
                weighted_data.append(data[j][1] * weight)
                weights.append(weight)
            except IndexError:
                pass
        weighted_average = sum(weighted_data) / sum(weights)
        smooth_data.append((data[i][0], weighted_average))
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
    elif daterange >= timedelta(days=700):
        majorlocator = dates.YearLocator()
        majorformatter = dates.DateFormatter("%Y")
        minorlocator = dates.MonthLocator(bymonth=(1, 4, 7, 10))
    elif daterange >= timedelta(days=200):
        majorlocator = dates.MonthLocator(bymonth=(1, 4, 7, 10))
        majorformatter = dates.DateFormatter("%b %Y")
        minorlocator = dates.MonthLocator()
    elif daterange >= timedelta(days=50):
        majorlocator = dates.MonthLocator()
        majorformatter = dates.DateFormatter("%b %Y")
        minorlocator = dates.WeekdayLocator(byweekday=6)
    else:
        majorlocator = dates.WeekdayLocator(byweekday=6)
        majorformatter = dates.DateFormatter("%d %b")
        minorlocator = dates.DayLocator()
    return majorlocator, majorformatter, minorlocator
