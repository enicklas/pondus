# -*- coding: UTF-8 -*-

"""
This file is part of Pondus, a personal weight manager.
Copyright (C) 2007-11  Eike Nicklas <eike@ephys.de>

This program is free software licensed under the MIT license. For details
see LICENSE or http://www.opensource.org/licenses/mit-license.php
"""

import os

from pondus.core import parameters
from pondus.core.all_datasets import AllDatasets
from pondus.backends.util import get_backend


class Person(object):
    """Implements the structure to store the user data."""

    def __init__(self, filepath=None):
        """Creates a new person object from the xml file at filepath."""
        self.height = 0.0
        self.measurements = AllDatasets()
        self.plan = AllDatasets()
        self.backend = get_backend('xml')
        if filepath is not None:
            self._read_from_file(filepath)

    def write_to_file(self, filepath):
        """Writes the person data to the xml file."""
        self.backend.write(self, filepath)

    def _read_from_file(self, filepath):
        """Reads data from the xml-file in filepath and adds it to the
        person object."""
        # if the standard file or the custom file exists, read from it
        if os.path.isfile(filepath):
            self._merge(self.backend.read(filepath))
            return
        # if using a custom file, that does not exist, start with empty data
        elif parameters.use_custom_file:
            return
        # if none of the above, try to import from the legacy data structure
        elif os.path.isfile(parameters.datafile_old):
            backend = get_backend('xml_old')
            self._merge(backend.read(parameters.datafile_old,
                                    parameters.planfile_old))
            return
        # this is the first start of pondus, start with empty data

    def _merge(self, other_person):
        """Merge data from other_person into self."""
        self.height = other_person.height
        self.measurements = other_person.measurements
        self.plan = other_person.plan
