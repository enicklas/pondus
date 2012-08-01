# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2011-12 Eike Nicklas <eike@ephys.de>

This program is free software licensed under the MIT license. For details
see LICENSE or http://www.opensource.org/licenses/mit-license.php
"""


imexport_backends = ('csv', 'sportstracker')


def get_backend(name):
    """Returns a backend corresponding to name. Possible names are:
    xml, xml_old, csv, sportstracker"""
    if name == 'xml':
        from .xml_backend import XmlBackend as Backend
    elif name == 'xml_old':
        from .xml_backend_old import XmlBackendOld as Backend
    elif name == 'csv':
        from .csv_backend import CsvBackend as Backend
    elif name == 'sportstracker':
        from .sportstracker_backend import SportstrackerBackend as Backend
    return Backend()
