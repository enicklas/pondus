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

from pondus import parameters

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
