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

from pondus.core import parameters


def sort_function_weight(listmodel, iter1, iter2, data):
    """Sorts the weight column correctly, i.e. interprets the weight
    data as floats instead of strings."""
    weight1 = float(listmodel.get_value(iter1, 2))
    weight2 = float(listmodel.get_value(iter2, 2))
    return cmp(weight1, weight2)


def register_icons():
    """Adds custom icons to the list of stock IDs."""
    icon_info = {'pondus_plot': parameters.plot_button_path}
    iconfactory = gtk.IconFactory()
    stock_ids = gtk.stock_list_ids()
    for stock_id in icon_info:
        # only load image files when our stock_id is not present
        if stock_id not in stock_ids:
            icon_file = icon_info[stock_id]
            pixbuf = gtk.gdk.pixbuf_new_from_file(icon_file)
            iconset = gtk.IconSet(pixbuf)
            iconfactory.add(stock_id, iconset)
    iconfactory.add_default()


def get_tooltip(dataset):
    """Returns a string containing the data of the optional parameters
    of the dataset."""

    def append_to_tooltip(tooltip, text):
        if tooltip != '':
            tooltip += '\n'
        return tooltip + text

    tooltip = ''
    if dataset.bodyfat is not None:
        text = _('Bodyfat') + ': ' + str(round(dataset.bodyfat,1)) + '%'
        tooltip = append_to_tooltip(tooltip, text)
    if dataset.muscle is not None:
        text = _('Muscle') + ': ' + str(round(dataset.muscle,1)) + '%'
        tooltip = append_to_tooltip(tooltip, text)
    if dataset.water is not None:
        text = _('Water') + ': ' + str(round(dataset.water,1)) + '%'
        tooltip = append_to_tooltip(tooltip, text)
    if dataset.note is not None:
        text = _('Note') + ': ' + dataset.note
        tooltip = append_to_tooltip(tooltip, text)
    if tooltip == '':
        return None
    return tooltip
