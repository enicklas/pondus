# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2011  Eike Nicklas <eike@ephys.de>

This program is free software licensed under the MIT license. For details
see LICENSE or http://www.opensource.org/licenses/mit-license.php
"""


def get_backend(name):
    """Returns a backend corresponding to name. Possible names are:
    xml, xml_old, csv"""
    if name == 'xml':
        from xml_backend import XmlBackend
        return XmlBackend()
    elif name == 'xml_old':
        from xml_backend_old import XmlBackendOld
        return XmlBackendOld()
    elif name == 'csv':
        from csv_backend import CsvBackend
        return CsvBackend()
