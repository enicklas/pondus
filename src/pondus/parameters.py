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

import os

# path of configuration and data files
configfile = os.path.expanduser('~/.config/pondus/pondusrc')
userdatafile = os.path.expanduser('~/.pondus/user_data.xml')
# legacy filepaths
datafile_old = os.path.expanduser('~/.pondus/datasets.xml')
planfile_old = os.path.expanduser('~/.pondus/weight-plan.xml')
# using standard or custom location for datafile?
use_custom_file = False

# configuration
config_default = {'window.remember_size': False,
                  'window.width': 180,
                  'window.height': 300,
                  'preferences.unit_system': 'metric',
                  'preferences.use_weight_plan': False}
config = dict(config_default)
have_mpl = False
convert_weight_data_to_kg = False

# tags used in the xml file and dataset objects
keys_required = ('id', 'date', 'weight')
keys_optional = ()

# paths to button/logo icons used
plot_button_path = 'usr/share/pondus/plot.png'
logo_path = '/usr/share/icons/hicolor/48x48/apps/pondus.png'
